# @app.get("/movies/titles")
# def get_movie_titles():
#     global df

#     if df is None:
#         raise HTTPException(
#             status_code=500,
#             detail="Movie dataset not loaded"
#         )

#     # Support your primaryTitle column
#     title_col = (
#         "primaryTitle" if "primaryTitle" in df.columns
#         else "title" if "title" in df.columns
#         else None
#     )

#     if title_col is None:
#         raise HTTPException(
#             status_code=500,
#             detail="No movie title column found"
#         )

#     titles = (
#         df[title_col]
#         .dropna()
#         .astype(str)
#         .str.strip()
#     )

#     titles = sorted(
#         titles[titles != ""].unique().tolist(),
#         key=str.casefold
#     )

#     return titles

# @app.get("/movies/titles")
# def get_movie_titles():
#     if df is None:
#         raise HTTPException(
#             status_code=500,
#             detail="Dataset is not loaded"
#         )

#     if "primaryTitle" not in df.columns:
#         raise HTTPException(
#             status_code=500,
#             detail=f"primaryTitle not found. Columns: {list(df.columns)}"
#         )

#     titles = (
#         df["primaryTitle"]
#         .dropna()
#         .astype(str)
#         .str.strip()
#     )

#     return sorted(
#         titles[titles != ""].unique().tolist(),
#         key=str.casefold
#     )

















import os
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from fastapi import FastAPI, HTTPException, Query
from sklearn.metrics.pairwise import cosine_similarity

# ==================================================
# CONFIGURATION
# ==================================================

BASE_DIR = Path(__file__).resolve().parent
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "").strip()
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

app = FastAPI(title="CineMatch Movie Recommendation API")

# ==================================================
# LOAD SAVED TF-IDF MODEL
# Keep these files beside main.py, or set MODEL_DIR.
# ==================================================

MODEL_DIR = Path(os.getenv("MODEL_DIR", str(BASE_DIR)))

def load_pickle(filename):
    path = MODEL_DIR / filename
    if not path.exists():
        return None
    with path.open("rb") as file:
        return pickle.load(file)

try:
    movies = load_pickle("movies.pkl")
    tfidf_matrix = load_pickle("tfidf_matrix.pkl")
    indices = load_pickle("indices.pkl")
except Exception as exc:
    print(f"Model loading error: {exc}")
    movies = None
    tfidf_matrix = None
    indices = None

if movies is not None:
    movies = movies.reset_index(drop=True)

# ==================================================
# HELPERS
# ==================================================

def require_model():
    if movies is None or tfidf_matrix is None or indices is None:
        raise HTTPException(
            status_code=500,
            detail=(
                "TF-IDF model files could not be loaded. "
                "Check movies.pkl, tfidf_matrix.pkl, indices.pkl "
                "and MODEL_DIR."
            ),
        )

def get_title_column():
    if movies is None:
        return None
    for column in ("primaryTitle", "title"):
        if column in movies.columns:
            return column
    return None

def tmdb_request(endpoint, params=None):
    if not TMDB_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="TMDB_API_KEY is missing from the backend environment.",
        )

    request_params = dict(params or {})
    request_params["api_key"] = TMDB_API_KEY

    try:
        response = requests.get(
            f"{TMDB_BASE_URL}{endpoint}",
            params=request_params,
            timeout=25,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        status = getattr(getattr(exc, "response", None), "status_code", None)
        raise HTTPException(
            status_code=502,
            detail=f"TMDB request failed (HTTP {status or 'connection error'}).",
        ) from exc

def image_url(path):
    if not path:
        return None
    return f"{TMDB_IMAGE_BASE}{path}"

def clean_tmdb_movie(movie):
    return {
        "tmdb_id": movie.get("id"),
        "id": movie.get("id"),
        "title": movie.get("title") or movie.get("name") or "Unknown",
        "poster_path": movie.get("poster_path"),
        "poster_url": image_url(movie.get("poster_path")),
        "backdrop_url": image_url(movie.get("backdrop_path")),
        "release_date": movie.get("release_date", ""),
        "vote_average": movie.get("vote_average"),
        "overview": movie.get("overview", ""),
        "genre_ids": movie.get("genre_ids", []),
    }

def search_tmdb_title(title):
    data = tmdb_request(
        "/search/movie",
        {"query": title, "page": 1, "include_adult": False},
    )
    results = data.get("results", [])
    if not results:
        return None

    wanted = title.strip().casefold()
    exact = next(
        (
            movie for movie in results
            if (movie.get("title") or "").strip().casefold() == wanted
        ),
        None,
    )
    return clean_tmdb_movie(exact or results[0])

def find_local_title(title):
    require_model()
    title_col = get_title_column()

    if title_col is None:
        return None

    titles = movies[title_col].fillna("").astype(str)
    wanted = title.strip().casefold()

    matches = titles[titles.str.strip().str.casefold() == wanted]
    if not matches.empty:
        return int(matches.index[0])

    return None

def local_tfidf_recommendations(title, top_n=10):
    require_model()

    title_col = get_title_column()
    if title_col is None:
        raise HTTPException(
            status_code=500,
            detail="The saved movie dataset has no title column.",
        )

    row_index = find_local_title(title)
    if row_index is None:
        return []

    similarities = cosine_similarity(
        tfidf_matrix[row_index],
        tfidf_matrix,
    ).flatten()

    # Exclude the selected movie itself.
    similarities[row_index] = -1
    ranked_indices = np.argsort(similarities)[::-1]

    recommendations = []
    for index in ranked_indices:
        score = float(similarities[index])

        if score <= 0:
            continue

        movie_title = str(movies.iloc[index][title_col]).strip()
        if not movie_title:
            continue

        recommendations.append({
            "title": movie_title,
            "score": round(score, 4),
        })

        if len(recommendations) >= top_n:
            break

    return recommendations

# ==================================================
# BASIC STATUS
# ==================================================

@app.get("/")
def root():
    return {
        "message": "CineMatch API is running",
        "model_loaded": (
            movies is not None
            and tfidf_matrix is not None
            and indices is not None
        ),
        "tmdb_key_configured": bool(TMDB_API_KEY),
    }

@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": (
            movies is not None
            and tfidf_matrix is not None
            and indices is not None
        ),
    }

# ==================================================
# LOCAL DATASET TITLES
# ==================================================

@app.get("/movies/titles")
def get_movie_titles():
    if movies is None:
        raise HTTPException(
            status_code=500,
            detail="Movie dataset is not loaded. Check movies.pkl.",
        )

    title_col = get_title_column()
    if title_col is None:
        raise HTTPException(
            status_code=500,
            detail=f"No title column found. Available: {list(movies.columns)}",
        )

    titles = (
        movies[title_col]
        .dropna()
        .astype(str)
        .str.strip()
    )

    return sorted(
        titles[titles != ""].drop_duplicates().tolist(),
        key=str.casefold,
    )

# ==================================================
# TMDB SEARCH
# ==================================================

@app.get("/tmdb/search")
def tmdb_search(
    query: str = Query(..., min_length=1),
    page: int = Query(1, ge=1, le=500),
):
    data = tmdb_request(
        "/search/movie",
        {
            "query": query.strip(),
            "page": page,
            "include_adult": False,
        },
    )

    return {
        "page": data.get("page", page),
        "total_pages": data.get("total_pages", 0),
        "total_results": data.get("total_results", 0),
        "results": [
            clean_tmdb_movie(movie)
            for movie in data.get("results", [])
        ],
    }

# ==================================================
# HOME FEED
# ==================================================

@app.get("/home")
def home(
    category: str = "trending",
    limit: int = Query(24, ge=1, le=50),
):
    allowed = {
        "trending": "/trending/movie/week",
        "popular": "/movie/popular",
        "top_rated": "/movie/top_rated",
        "now_playing": "/movie/now_playing",
        "upcoming": "/movie/upcoming",
    }

    if category not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported category. Choose from {list(allowed)}",
        )

    data = tmdb_request(allowed[category], {"page": 1})

    return {
        "results": [
            clean_tmdb_movie(movie)
            for movie in data.get("results", [])[:limit]
        ]
    }

# ==================================================
# MOVIE DETAILS
# ==================================================

@app.get("/movie/id/{tmdb_id}")
def movie_details(tmdb_id: int):
    if tmdb_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid TMDB movie ID.")

    movie = tmdb_request(f"/movie/{tmdb_id}")
    result = clean_tmdb_movie(movie)

    result["genres"] = movie.get("genres", [])
    result["runtime"] = movie.get("runtime")
    result["tagline"] = movie.get("tagline", "")
    result["imdb_id"] = movie.get("imdb_id")

    return result

# ==================================================
# TF-IDF RECOMMENDATIONS
# ==================================================

@app.get("/recommend/tfidf")
def recommend_tfidf(
    title: str = Query(..., min_length=1),
    top_n: int = Query(10, ge=1, le=50),
):
    recommendations = local_tfidf_recommendations(title, top_n)

    if not recommendations and find_local_title(title) is None:
        return []

    return recommendations

# ==================================================
# COMBINED TF-IDF + GENRE RECOMMENDATIONS
# ==================================================

@app.get("/movie/search")
def movie_recommendation_bundle(
    query: str = Query(..., min_length=1),
    tfidf_top_n: int = Query(10, ge=1, le=20),
    genre_limit: int = Query(10, ge=1, le=20),
):
    # Resolve the chosen TMDB title and genres.
    selected_movie = search_tmdb_title(query)
    if selected_movie is None:
        raise HTTPException(
            status_code=404,
            detail=f"No TMDB movie found for '{query}'.",
        )

    # TF-IDF model is trained on local movie titles.
    local_recs = local_tfidf_recommendations(query, tfidf_top_n)

    # Match each local recommendation to TMDB for its poster and ID.
    tfidf_cards = []
    for item in local_recs:
        try:
            tmdb_match = search_tmdb_title(item["title"])
        except HTTPException:
            tmdb_match = None

        if tmdb_match:
            tfidf_cards.append({
                "title": item["title"],
                "score": item["score"],
                "tmdb": tmdb_match,
            })

    # Find genre recommendations using the selected movie's TMDB genres.
    details = tmdb_request(f"/movie/{selected_movie['tmdb_id']}")
    genre_ids = [
        str(genre["id"])
        for genre in details.get("genres", [])
        if genre.get("id")
    ]

    genre_cards = []
    if genre_ids:
        data = tmdb_request(
            "/discover/movie",
            {
                "with_genres": ",".join(genre_ids),
                "sort_by": "vote_count.desc",
                "vote_count.gte": 50,
                "include_adult": False,
                "page": 1,
            },
        )

        for movie in data.get("results", []):
            if movie.get("id") == selected_movie["tmdb_id"]:
                continue
            genre_cards.append(clean_tmdb_movie(movie))
            if len(genre_cards) >= genre_limit:
                break

    return {
        "selected_movie": selected_movie,
        "tfidf_recommendations": tfidf_cards,
        "genre_recommendations": genre_cards,
    }
