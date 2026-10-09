
# import os
# import requests
# import streamlit as st
# from urllib.parse import quote_plus
# # =============================
# # CONFIGURATION
# # =============================
# API_BASE = os.getenv(
#     "API_BASE_URL",
#     "https://movie-rec-466x.onrender.com"
# )
# TMDB_IMG = "https://image.tmdb.org/t/p/w500"

# st.set_page_config(
#     page_title="CineMatch | Movie Recommender",
#     page_icon="🎬",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# # =============================
# # CSS - DARK CINEMATIC THEME
# # =============================
# st.markdown("""
# <style>
# .stApp {
#     background: #080d17;
#     color: #f5f5f5;
# }
# .block-container {
#     max-width: 1500px;
#     padding-top: 1.2rem;
#     padding-bottom: 3rem;
# }
# [data-testid="stSidebar"] {
#     background: #0d1422;
#     border-right: 1px solid #202b3c;
# }
# [data-testid="stSidebar"] * {
#     color: #f5f5f5;
# }
# h1, h2, h3 {
#     color: #ffffff !important;
# }
# p, label {
#     color: #d2d8e2;
# }
# .stTextInput input {
#     background: #151e2e;
#     color: white;
#     border: 1px solid #303d52;
#     border-radius: 12px;
# }
# .stButton button {
#     width: 100%;
#     border-radius: 9px;
#     border: 1px solid #303d52;
#     background: #151e2e;
#     color: white;
#     transition: 0.2s;
# }
# .stButton button:hover {
#     background: #e50914;
#     color: white;
#     border-color: #e50914;
# }
# .movie-card {
#     background: #111a29;
#     padding: 9px;
#     border-radius: 12px;
#     border: 1px solid #202d40;
#     margin-bottom: 8px;
# }
# .movie-name {
#     color: #f5f5f5;
#     font-size: 0.9rem;
#     font-weight: 600;
#     min-height: 40px;
#     padding-top: 7px;
# }
# .muted {
#     color: #9ca9bc;
#     font-size: 0.9rem;
# }
# .hero {
#     padding: 25px;
#     border-radius: 18px;
#     background: linear-gradient(110deg, #172337, #111827);
#     border: 1px solid #29374c;
#     margin-bottom: 20px;
# }
# div[data-testid="stImage"] img {
#     border-radius: 10px;
# }
# hr {
#     border-color: #263246;
# }
# </style>
# """, unsafe_allow_html=True)

# # =============================
# # SESSION STATE
# # =============================
# if "view" not in st.session_state:
#     st.session_state.view = "home"

# if "selected_tmdb_id" not in st.session_state:
#     st.session_state.selected_tmdb_id = None

# if "search_text" not in st.session_state:
#     st.session_state.search_text = ""

# # Support browser URL navigation
# qp_view = st.query_params.get("view")
# qp_id = st.query_params.get("id")

# if qp_view in ("home", "details"):
#     st.session_state.view = qp_view

# if qp_id:
#     try:
#         st.session_state.selected_tmdb_id = int(qp_id)
#         st.session_state.view = "details"
#     except (ValueError, TypeError):
#         pass


# def goto_home():
#     st.session_state.view = "home"
#     st.session_state.selected_tmdb_id = None
#     st.query_params["view"] = "home"
#     if "id" in st.query_params:
#         del st.query_params["id"]
#     st.rerun()


# def goto_details(tmdb_id):
#     st.session_state.selected_tmdb_id = int(tmdb_id)
#     st.session_state.view = "details"
#     st.query_params["view"] = "details"
#     st.query_params["id"] = str(tmdb_id)
#     st.rerun()


# # =============================
# # API REQUESTS
# # =============================
# @st.cache_data(ttl=300, show_spinner=False)
# def api_get_json(path, params=None):
#     try:
#         response = requests.get(
#             f"{API_BASE}{path}",
#             params=params,
#             timeout=40,
#         )
#         response.raise_for_status()
#         return response.json(), None
#     except requests.RequestException as e:
#         return None, str(e)
#     except ValueError as e:
#         return None, f"Invalid API response: {e}"


# def normalize_cards(data):
#     """Support TMDB results and backend movie-card responses."""
#     if isinstance(data, dict):
#         items = data.get("results", [])
#     elif isinstance(data, list):
#         items = data
#     else:
#         return []

#     cards = []

#     for movie in items:
#         tmdb_id = movie.get("tmdb_id") or movie.get("id")
#         title = movie.get("title") or movie.get("name")

#         if not tmdb_id or not title:
#             continue

#         poster = movie.get("poster_url")

#         if not poster and movie.get("poster_path"):
#             poster = f"{TMDB_IMG}{movie['poster_path']}"

#         cards.append({
#             "tmdb_id": int(tmdb_id),
#             "title": title,
#             "poster_url": poster,
#             "release_date": movie.get("release_date", ""),
#             "vote_average": movie.get("vote_average"),
#         })

#     return cards


# # =============================
# # MOVIE POSTER GRID
# # =============================
# def poster_grid(cards, cols=6, key_prefix="movies"):
#     if not cards:
#         st.info("No movies found.")
#         return

#     cols = max(1, min(cols, 8))

#     for start in range(0, len(cards), cols):
#         row = cards[start:start + cols]
#         columns = st.columns(cols)

#         for position, movie in enumerate(row):
#             with columns[position]:
#                 poster = movie.get("poster_url")
#                 title = movie.get("title", "Unknown")
#                 movie_id = movie.get("tmdb_id")

#                 if poster:
#                     st.image(poster, use_container_width=True)
#                 else:
#                     st.markdown(
#                         "<div style='height:220px;background:#172337;"
#                         "border-radius:10px;display:flex;align-items:center;"
#                         "justify-content:center;color:#9ca9bc'>"
#                         "Poster unavailable</div>",
#                         unsafe_allow_html=True,
#                     )

#                 st.markdown(
#                     f"<div class='movie-name'>{title}</div>",
#                     unsafe_allow_html=True,
#                 )

#                 rating = movie.get("vote_average")
#                 if rating is not None:
#                     st.caption(f"⭐ {float(rating):.1f}/10")

#                 if movie_id and st.button(
#                     "View movie",
#                     key=f"{key_prefix}_{start}_{position}_{movie_id}",
#                 ):
#                     goto_details(movie_id)


# # =============================
# # TF-IDF RECOMMENDATION CARDS
# # =============================
# def tfidf_items_to_cards(items):
#     cards = []

#     for item in items or []:
#         tmdb = item.get("tmdb") or {}

#         if not tmdb.get("tmdb_id"):
#             continue

#         cards.append({
#             "tmdb_id": tmdb["tmdb_id"],
#             "title": tmdb.get("title") or item.get("title", "Unknown"),
#             "poster_url": tmdb.get("poster_url"),
#             "score": item.get("score", 0),
#         })

#     return cards


# # =============================
# # SIDEBAR
# # =============================
# with st.sidebar:
#     st.markdown("# 🎬 CineMatch")
#     st.caption("Discover your next favourite movie")
#     st.divider()

#     if st.button("🏠 Home", use_container_width=True):
#         goto_home()

#     st.markdown("### Explore")

#     category = st.selectbox(
#         "Movie collection",
#         [
#             "trending",
#             "popular",
#             "top_rated",
#             "now_playing",
#             "upcoming",
#         ],
#         format_func=lambda x: x.replace("_", " ").title(),
#     )

#     grid_cols = st.slider("Posters per row", 3, 8, 6)

#     st.divider()
#     st.caption("Powered by TMDB + TF-IDF")


# # =============================
# # HEADER
# # =============================
# st.markdown("# 🎬 CineMatch")
# st.markdown(
#     "<p class='muted'>Find movies you love. Discover movies you'll love next.</p>",
#     unsafe_allow_html=True,
# )

# search_query = st.text_input(
#     "Search movies",
#     placeholder="Search titles — K.G.F, Pushpa, Interstellar...",
#     key="movie_search",
# )
# # =============================
# # SELECT MOVIE FROM LOCAL DATASET
# # =============================
# @st.cache_data(ttl=600)
# def get_local_movie_titles():
#     data, error = api_get_json("/movies/titles")

#     if error or not isinstance(data, list):
#         return []

#     return data


# st.markdown("## 🎞️ Choose a Movie from Your Dataset")

# movie_titles = get_local_movie_titles()

# if movie_titles:
#     selected_title = st.selectbox(
#         "Select movie title",
#         options=movie_titles,
#         index=None,
#         placeholder="Choose a movie...",
#         key="local_movie_select",
#     )

#     if st.button("▶ Enter", key="enter_selected_movie"):
#         if selected_title:
#             # Search TMDB for the selected local title
#             search_data, search_error = api_get_json(
#                 "/tmdb/search",
#                 {"query": selected_title, "page": 1},
#             )

#             cards = normalize_cards(search_data)

#             if cards:
#                 # Prefer an exact title match when available
#                 exact_match = next(
#                     (
#                         movie for movie in cards
#                         if movie["title"].casefold()
#                         == selected_title.casefold()
#                     ),
#                     cards[0],
#                 )

#                 goto_details(exact_match["tmdb_id"])
#             else:
#                 st.warning(
#                     "Could not find this movie on TMDB. "
#                     "Try another title."
#                 )
# else:
#     st.warning(
#         "Could not load local movie titles. "
#         "Check that your FastAPI backend is running."
#     )
# # =============================
# # SEARCH RESULTS
# # =============================
# if search_query.strip():
#     query = search_query.strip()

#     st.markdown(f"## Search results for **{query}**")

#     if len(query) < 2:
#         st.info("Type at least two characters.")
#     else:
#         with st.spinner("Searching movies..."):
#             search_data, search_error = api_get_json(
#                 "/tmdb/search",
#                 {"query": query, "page": 1},
#             )

#         if search_error:
#             st.error(f"Movie search failed: {search_error}")
#         else:
#             search_cards = normalize_cards(search_data)

#             if search_cards:
#                 poster_grid(
#                     search_cards[:24],
#                     cols=grid_cols,
#                     key_prefix="search",
#                 )
#             else:
#                 st.info("No matching movies found.")

# # =============================
# # HOME FEED
# # =============================
# elif st.session_state.view == "home":
#     home_data, home_error = api_get_json(
#         "/home",
#         {"category": category, "limit": 24},
#     )

#     if home_error:
#         st.error(f"Could not load movies: {home_error}")
#         st.info(
#             "Check that your FastAPI backend is running and the "
#             "TMDB API key is configured."
#         )
#     else:
#         home_cards = normalize_cards(home_data)

#         if home_cards:
#             featured = home_cards[0]

#             # Featured movie banner
#             st.markdown("<div class='hero'>", unsafe_allow_html=True)

#             hero_left, hero_right = st.columns([2, 1])

#             with hero_left:
#                 st.caption(f"🔥 FEATURED · {category.upper()}")
#                 st.markdown(f"# {featured['title']}")

#                 if featured.get("release_date"):
#                     st.write(
#                         f"Release date: {featured['release_date']}"
#                     )

#                 if st.button(
#                     "▶ Explore movie",
#                     key="featured_movie",
#                 ):
#                     goto_details(featured["tmdb_id"])

#             with hero_right:
#                 if featured.get("poster_url"):
#                     st.image(
#                         featured["poster_url"],
#                         use_container_width=True,
#                     )

#             st.markdown("</div>", unsafe_allow_html=True)

#             st.markdown(f"## 🔥 {category.replace('_', ' ').title()} Movies")
#             poster_grid(
#                 home_cards,
#                 cols=grid_cols,
#                 key_prefix="home",
#             )
#         else:
#             st.info("No movies available right now.")

# # =============================
# # MOVIE DETAILS + RECOMMENDATIONS
# # =============================
# if (
#     st.session_state.view == "details"
#     and st.session_state.selected_tmdb_id
# ):
#     tmdb_id = st.session_state.selected_tmdb_id

#     st.divider()

#     if st.button("← Back to Home", key="back_home"):
#         goto_home()

#     with st.spinner("Loading movie details..."):
#         details, details_error = api_get_json(
#             f"/movie/id/{tmdb_id}"
#         )

#     if details_error or not details:
#         st.error(f"Could not load movie details: {details_error}")
#     else:
#         left, right = st.columns([1, 2.2], gap="large")

#         with left:
#             if details.get("poster_url"):
#                 st.image(
#                     details["poster_url"],
#                     use_container_width=True,
#                 )
#             else:
#                 st.info("Poster unavailable.")

#         with right:
#             st.markdown(f"# {details.get('title', 'Movie')}")

#             release = details.get("release_date") or "Unknown"
#             genres = ", ".join(
#                 genre.get("name", "")
#                 for genre in details.get("genres", [])
#             ) or "Unknown"

#             st.markdown(f"**Release date:** {release}")
#             st.markdown(f"**Genres:** {genres}")

#             st.markdown("### Story")
#             st.write(
#                 details.get("overview")
#                 or "No overview available."
#             )

#         if details.get("backdrop_url"):
#             with st.expander("View movie backdrop"):
#                 st.image(
#                     details["backdrop_url"],
#                     use_container_width=True,
#                 )

#         st.divider()
#         st.markdown("## 🎯 Recommended for You")
#         st.caption(
#             "Recommendations are recalculated for the movie you select."
#         )

#         # Bundle endpoint: explicitly request 10 TF-IDF results
#         selected_title = details.get("title", "").strip()

#         with st.spinner("Finding similar movies..."):
#             bundle, bundle_error = api_get_json(
#                 "/movie/search",
#                 {
#                     "query": selected_title,
#                     "tfidf_top_n": 10,
#                     "genre_limit": 10,
#                 },
#             )

#         if bundle_error or not bundle:
#             st.warning(
#                 "Could not load the complete recommendation bundle. "
#                 "Trying the TF-IDF endpoint directly."
#             )

#             with st.spinner("Calculating cosine similarity..."):
#                 tfidf_data, tfidf_error = api_get_json(
#                     "/recommend/tfidf",
#                     {"title": selected_title, "top_n": 10},
#                 )

#             if tfidf_error:
#                 st.error(
#                     "TF-IDF recommendations failed. "
#                     "The selected TMDB title may not exist in your "
#                     "local dataset. Check that movie's title in df.pkl."
#                 )
#             else:
#                 st.write(
#                     "The direct TF-IDF endpoint returns titles and "
#                     "scores only; posters require TMDB matching."
#                 )

#                 for rank, item in enumerate(tfidf_data or [], 1):
#                     st.write(
#                         f"{rank}. {item['title']} — "
#                         f"cosine similarity: {item['score']:.3f}"
#                     )

#         else:
#             # TOP 10 COSINE SIMILARITY MOVIES
#             st.markdown("### 🧠 Top 10 Similar Movies")
#             st.caption(
#                 "Ranked by cosine similarity from your local TF-IDF model."
#             )

#             tfidf_cards = tfidf_items_to_cards(
#                 bundle.get("tfidf_recommendations", [])
#             )

#             if tfidf_cards:
#                 poster_grid(
#                     tfidf_cards[:10],
#                     cols=grid_cols,
#                     key_prefix=f"tfidf_{tmdb_id}",
#                 )
#             else:
#                 st.info(
#                     "No TF-IDF recommendations were found for this title."
#                 )

#             # GENRE RECOMMENDATIONS
#             st.divider()
#             st.markdown("### 🎭 More Movies in This Genre")

#             genre_cards = normalize_cards(
#                 bundle.get("genre_recommendations", [])
#             )

#             if genre_cards:
#                 poster_grid(
#                     genre_cards[:10],
#                     cols=grid_cols,
#                     key_prefix=f"genre_{tmdb_id}",
#                 )
#             else:
#                 st.info("No genre recommendations available.")

# st.divider()
# st.markdown(
#     "<div style='text-align:center;color:#8290a5;font-size:0.85rem'>"
#     "CineMatch · Movie discovery powered by TMDB and TF-IDF"
#     "</div>",
#     unsafe_allow_html=True,
# )







import os
import html
from urllib.parse import quote_plus

import requests
import streamlit as st

# ==================================================
# CONFIGURATION
# ==================================================

API_BASE = os.getenv(
    "API_BASE_URL",
    "https://movie-rec-466x.onrender.com",
).rstrip("/")

TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(
    page_title="CineMatch | Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==================================================
# CSS
# ==================================================

st.markdown("""
<style>
.stApp {
    background: #080d17;
    color: #f5f5f5;
}
.block-container {
    max-width: 1500px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}
[data-testid="stSidebar"] {
    background: #0d1422;
    border-right: 1px solid #202b3c;
}
[data-testid="stSidebar"] * {
    color: #f5f5f5;
}
h1, h2, h3 {
    color: #ffffff !important;
}
p, label {
    color: #d2d8e2;
}
.stTextInput input {
    background: #151e2e;
    color: white;
    border: 1px solid #303d52;
    border-radius: 12px;
}
.stButton button {
    width: 100%;
    border-radius: 9px;
    border: 1px solid #303d52;
    background: #151e2e;
    color: white;
    transition: 0.2s;
}
.stButton button:hover {
    background: #e50914;
    color: white;
    border-color: #e50914;
}
.movie-name {
    color: #f5f5f5;
    font-size: 0.9rem;
    font-weight: 600;
    min-height: 40px;
    padding-top: 7px;
    overflow-wrap: anywhere;
}
.muted {
    color: #9ca9bc;
    font-size: 0.9rem;
}
.hero {
    padding: 25px;
    border-radius: 18px;
    background: linear-gradient(110deg, #172337, #111827);
    border: 1px solid #29374c;
    margin-bottom: 20px;
}
div[data-testid="stImage"] img {
    border-radius: 10px;
}
hr {
    border-color: #263246;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# SESSION STATE AND NAVIGATION
# ==================================================

if "view" not in st.session_state:
    st.session_state.view = "home"

if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None

def goto_home():
    st.session_state.view = "home"
    st.session_state.selected_tmdb_id = None
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()

def goto_details(tmdb_id):
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.session_state.view = "details"
    st.query_params["view"] = "details"
    st.query_params["id"] = str(tmdb_id)
    st.rerun()

qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")

if qp_view in ("home", "details"):
    st.session_state.view = qp_view

if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except (ValueError, TypeError):
        pass

# ==================================================
# API REQUESTS
# ==================================================

def api_get_json(path, params=None):
    try:
        response = requests.get(
            f"{API_BASE}{path}",
            params=params,
            timeout=45,
        )
        response.raise_for_status()
        return response.json(), None

    except requests.HTTPError as exc:
        response = exc.response
        message = f"HTTP {response.status_code}"

        try:
            detail = response.json().get("detail")
            if detail:
                message += f": {detail}"
        except (ValueError, AttributeError):
            message += f": {response.text[:300]}"

        return None, message

    except requests.RequestException as exc:
        return None, str(exc)

    except ValueError as exc:
        return None, f"Invalid JSON response: {exc}"

# ==================================================
# NORMALIZE MOVIE DATA
# ==================================================

def normalize_cards(data):
    if isinstance(data, dict):
        items = data.get("results", [])
    elif isinstance(data, list):
        items = data
    else:
        return []

    cards = []

    for movie in items:
        if not isinstance(movie, dict):
            continue

        movie_id = movie.get("tmdb_id") or movie.get("id")
        title = movie.get("title") or movie.get("name")

        if not movie_id or not title:
            continue

        try:
            movie_id = int(movie_id)
        except (ValueError, TypeError):
            continue

        poster = movie.get("poster_url")
        if not poster and movie.get("poster_path"):
            poster = f"{TMDB_IMG}{movie['poster_path']}"

        cards.append({
            "tmdb_id": movie_id,
            "title": str(title),
            "poster_url": poster,
            "release_date": movie.get("release_date") or "",
            "vote_average": movie.get("vote_average"),
        })

    return cards

# ==================================================
# LOCAL DATASET TITLES
# ==================================================

def get_local_movie_titles():
    data, error = api_get_json("/movies/titles")

    if error:
        st.error(f"Could not load movie titles: {error}")
        return []

    if isinstance(data, list):
        return [
            str(title).strip()
            for title in data
            if title and str(title).strip()
        ]

    st.error("Unexpected response from /movies/titles.")
    return []

# ==================================================
# MOVIE POSTER GRID
# ==================================================

def poster_grid(cards, cols=6, key_prefix="movies"):
    if not cards:
        st.info("No movies found.")
        return

    cols = max(1, min(int(cols), 8))

    for start in range(0, len(cards), cols):
        row = cards[start:start + cols]
        columns = st.columns(cols)

        for position, movie in enumerate(row):
            with columns[position]:
                poster = movie.get("poster_url")
                title = movie.get("title", "Unknown")
                movie_id = movie.get("tmdb_id")

                if poster:
                    st.image(poster, use_container_width=True)
                else:
                    st.markdown(
                        "<div style='height:220px;background:#172337;"
                        "border-radius:10px;display:flex;"
                        "align-items:center;justify-content:center;"
                        "color:#9ca9bc'>Poster unavailable</div>",
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    f"<div class='movie-name'>"
                    f"{html.escape(str(title))}</div>",
                    unsafe_allow_html=True,
                )

                rating = movie.get("vote_average")
                if rating is not None:
                    try:
                        st.caption(f"⭐ {float(rating):.1f}/10")
                    except (ValueError, TypeError):
                        pass

                if movie_id and st.button(
                    "View movie",
                    key=f"{key_prefix}_{start}_{position}_{movie_id}",
                ):
                    goto_details(movie_id)

# ==================================================
# TF-IDF RECOMMENDATION CARDS
# ==================================================

def tfidf_items_to_cards(items):
    cards = []

    for item in items or []:
        if not isinstance(item, dict):
            continue

        tmdb = item.get("tmdb") or {}

        # Accept either the nested TMDB format or a flat card.
        movie_id = (
            tmdb.get("tmdb_id")
            or tmdb.get("id")
            or item.get("tmdb_id")
            or item.get("id")
        )

        title = (
            tmdb.get("title")
            or item.get("title")
            or "Unknown"
        )

        if not movie_id:
            continue

        poster = tmdb.get("poster_url") or item.get("poster_url")

        if not poster:
            poster_path = tmdb.get("poster_path") or item.get("poster_path")
            if poster_path:
                poster = f"{TMDB_IMG}{poster_path}"

        cards.append({
            "tmdb_id": movie_id,
            "title": title,
            "poster_url": poster,
            "vote_average": tmdb.get("vote_average"),
            "score": item.get("score", 0),
        })

    return cards

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:
    st.markdown("# 🎬 CineMatch")
    st.caption("Discover your next favourite movie")
    st.divider()

    if st.button("🏠 Home", use_container_width=True):
        goto_home()

    st.markdown("### Explore")

    category = st.selectbox(
        "Movie collection",
        [
            "trending",
            "popular",
            "top_rated",
            "now_playing",
            "upcoming",
        ],
        format_func=lambda value: value.replace("_", " ").title(),
    )

    grid_cols = st.slider("Posters per row", 3, 8, 6)

    st.divider()
    st.caption("Powered by TMDB + TF-IDF")

# ==================================================
# HEADER AND SEARCH
# ==================================================

st.markdown("# 🎬 CineMatch")
st.markdown(
    "<p class='muted'>Find movies you love. "
    "Discover movies you'll love next.</p>",
    unsafe_allow_html=True,
)

search_query = st.text_input(
    "Search movies",
    placeholder="Search titles — K.G.F, Pushpa, Interstellar...",
    key="movie_search",
)

# ==================================================
# CHOOSE MOVIE FROM YOUR LOCAL DATASET
# ==================================================

st.markdown("## 🎞️ Choose a Movie from Your Dataset")

movie_titles = get_local_movie_titles()

if movie_titles:
    selected_title = st.selectbox(
        "Select movie title",
        options=movie_titles,
        index=None,
        placeholder="Choose a movie...",
        key="local_movie_select",
    )

    if st.button("▶ Enter", key="enter_selected_movie"):
        if selected_title:
            with st.spinner("Finding the selected movie..."):
                search_data, search_error = api_get_json(
                    "/tmdb/search",
                    {"query": selected_title, "page": 1},
                )

            if search_error:
                st.error(f"TMDB search failed: {search_error}")
            else:
                cards = normalize_cards(search_data)

                exact_match = next(
                    (
                        movie for movie in cards
                        if movie["title"].strip().casefold()
                        == selected_title.strip().casefold()
                    ),
                    None,
                )

                if exact_match:
                    goto_details(exact_match["tmdb_id"])
                elif cards:
                    st.warning(
                        "No exact title match was found on TMDB. "
                        "Choose the correct movie from Search instead."
                    )
                    poster_grid(
                        cards[:10],
                        cols=min(grid_cols, 5),
                        key_prefix="local_search",
                    )
                else:
                    st.warning("TMDB did not find this movie.")
else:
    st.info(
        "Your local movie-title list is unavailable. "
        "Check the backend deployment and /movies/titles endpoint."
    )

# ==================================================
# SEARCH RESULTS
# ==================================================

if search_query.strip():
    query = search_query.strip()
    st.markdown(f"## Search results for **{query}**")

    if len(query) < 2:
        st.info("Type at least two characters.")
    else:
        with st.spinner("Searching movies..."):
            search_data, search_error = api_get_json(
                "/tmdb/search",
                {"query": query, "page": 1},
            )

        if search_error:
            st.error(f"Movie search failed: {search_error}")
        else:
            search_cards = normalize_cards(search_data)

            if search_cards:
                poster_grid(
                    search_cards[:24],
                    cols=grid_cols,
                    key_prefix="search",
                )
            else:
                st.info("No matching movies found.")

# ==================================================
# HOME FEED
# ==================================================

elif st.session_state.view == "home":
    with st.spinner("Loading movies..."):
        home_data, home_error = api_get_json(
            "/home",
            {"category": category, "limit": 24},
        )

    if home_error:
        st.error(f"Could not load movies: {home_error}")
        st.info(
            "Check the backend deployment and your TMDB_API_KEY."
        )
    else:
        home_cards = normalize_cards(home_data)

        if home_cards:
            featured = home_cards[0]

            st.markdown(
                "<div class='hero'>",
                unsafe_allow_html=True,
            )

            hero_left, hero_right = st.columns([2, 1])

            with hero_left:
                st.caption(f"🔥 FEATURED · {category.upper()}")
                st.markdown(f"# {featured['title']}")

                if featured.get("release_date"):
                    st.write(
                        f"Release date: {featured['release_date']}"
                    )

                if st.button(
                    "▶ Explore movie",
                    key="featured_movie",
                ):
                    goto_details(featured["tmdb_id"])

            with hero_right:
                if featured.get("poster_url"):
                    st.image(
                        featured["poster_url"],
                        use_container_width=True,
                    )

            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown(
                f"## 🔥 {category.replace('_', ' ').title()} Movies"
            )
            poster_grid(
                home_cards,
                cols=grid_cols,
                key_prefix="home",
            )
        else:
            st.info("No movies available right now.")

# ==================================================
# MOVIE DETAILS AND RECOMMENDATIONS
# ==================================================

# ==================================================
# MOVIE DETAILS AND RECOMMENDATIONS
# ==================================================

if (
    st.session_state.view == "details"
    and st.session_state.selected_tmdb_id
):
    tmdb_id = st.session_state.selected_tmdb_id

    st.divider()

    if st.button("← Back to Home", key="back_home"):
        goto_home()

    with st.spinner("Loading movie details..."):
        details, details_error = api_get_json(
            f"/movie/id/{tmdb_id}"
        )

    if details_error or not details:
        st.error(f"Could not load movie details: {details_error}")

    else:
        left, right = st.columns([1, 2.2], gap="large")

        with left:
            if details.get("poster_url"):
                st.image(
                    details["poster_url"],
                    use_container_width=True,
                )
            else:
                st.info("Poster unavailable.")

        with right:
            st.markdown(f"# {details.get('title', 'Movie')}")

            release = details.get("release_date") or "Unknown"

            genres = ", ".join(
                genre.get("name", "")
                for genre in details.get("genres", [])
            ) or "Unknown"

            rating = details.get("vote_average")

            if rating is not None:
                st.markdown(f"**Rating:** ⭐ {rating}/10")

            st.markdown(f"**Release date:** {release}")
            st.markdown(f"**Genres:** {genres}")

            runtime = details.get("runtime")
            if runtime:
                st.markdown(f"**Runtime:** {runtime} minutes")

            st.markdown("### Story")
            st.write(
                details.get("overview") or "No overview available."
            )

        if details.get("backdrop_url"):
            with st.expander("View movie backdrop"):
                st.image(
                    details["backdrop_url"],
                    use_container_width=True,
                )

        # ==================================================
        # WATCH LINKS
        # ==================================================

        movie_title = details.get("title", "Movie")
        encoded_title = quote_plus(movie_title)

        justwatch_url = (
            f"https://www.justwatch.com/in/search?q={encoded_title}"
        )

        trailer_url = (
            "https://www.youtube.com/results?search_query="
            f"{encoded_title}+official+trailer"
        )

        movie_url = (
            "https://www.youtube.com/results?search_query="
            f"{encoded_title}+full+movie"
        )

        song_url = (
            "https://www.youtube.com/results?search_query="
            f"{encoded_title}+movie+songs"
        )

        st.divider()
        st.markdown("### 🍿 Watch This Movie")

        watch_col1, watch_col2, watch_col3, watch_col4 = st.columns(4)

        with watch_col1:
            st.link_button(
                "▶ Watch Options",
                justwatch_url,
                use_container_width=True,
            )

        with watch_col2:
            st.link_button(
                "🎬 Watch Trailer",
                trailer_url,
                use_container_width=True,
            )

        with watch_col3:
            st.link_button(
                "📺 Search Full Movie",
                movie_url,
                use_container_width=True,
            )

        with watch_col4:
            st.link_button(
                "🎵 Search Songs",
                song_url,
                use_container_width=True,
            )

        # movie_title = details.get("title", "Movie")
        # encoded_title = quote_plus(movie_title)

        # justwatch_url = (
        #     f"https://www.justwatch.com/in/search?q={encoded_title}"
        # )

        # trailer_url = (
        #     "https://www.youtube.com/results?search_query="
        #     f"{encoded_title}+official+trailer"
        # )

        # movie_url = (
        #     "https://www.youtube.com/results?search_query="
        #     f"{encoded_title}+full+movie"
        # )

        # st.divider()
        # st.markdown("### 🍿 Watch This Movie")

        # watch_col1, watch_col2, watch_col3 = st.columns(3)

        # with watch_col1:
        #     st.link_button(
        #         "▶ Watch Options",
        #         justwatch_url,
        #         use_container_width=True,
        #     )

        # with watch_col2:
        #     st.link_button(
        #         "🎬 Watch Trailer",
        #         trailer_url,
        #         use_container_width=True,
        #     )

        # with watch_col3:
        #     st.link_button(
        #         "📺 Search Full Movie",
        #         movie_url,
        #         use_container_width=True,
        #     )

        # with watch_col3:
        #     st.link_button(
        #         "📺 Search Full Movie",
        #         movie_url,
        #         use_container_width=True,
        #     )
        # ==================================================
        # RECOMMENDATIONS
        # ==================================================

        st.divider()
        st.markdown("## 🎯 Recommended for You")

        st.caption(
            "TF-IDF recommendations use your local model. "
            "Genre recommendations use TMDB movie genres."
        )

        selected_title = details.get("title", "").strip()

        with st.spinner("Finding similar movies..."):
            bundle, bundle_error = api_get_json(
                "/movie/search",
                {
                    "query": selected_title,
                    "tfidf_top_n": 10,
                    "genre_limit": 10,
                },
            )

        if bundle_error:
            st.error(
                f"Could not load recommendations: {bundle_error}"
            )

        elif not bundle:
            st.warning(
                "The recommendation API returned no data."
            )

        else:
            # TF-IDF recommendations
            st.markdown("### 🧠 Top Similar Movies")

            tfidf_cards = tfidf_items_to_cards(
                bundle.get("tfidf_recommendations", [])
            )

            if tfidf_cards:
                poster_grid(
                    tfidf_cards[:10],
                    cols=grid_cols,
                    key_prefix=f"tfidf_{tmdb_id}",
                )
            else:
                st.info(
                    "No TF-IDF matches were found for this title "
                    "in your local dataset."
                )

            # Genre recommendations
            st.divider()
            st.markdown("### 🎭 More Movies in This Genre")

            genre_cards = normalize_cards(
                bundle.get("genre_recommendations", [])
            )

            if genre_cards:
                poster_grid(
                    genre_cards[:10],
                    cols=grid_cols,
                    key_prefix=f"genre_{tmdb_id}",
                )
            else:
                st.info("No genre recommendations available.")



# ==================================================
# FOOTER
# ==================================================

st.divider()
st.markdown(
    "<div style='text-align:center;color:#8290a5;font-size:0.85rem'>"
    "CineMatch · Movie discovery powered by TMDB and TF-IDF"
    "</div>",
    unsafe_allow_html=True,
)
