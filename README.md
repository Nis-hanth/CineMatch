# 🎬 CineMatch — Movie Recommendation System

![CineMatch Preview](assets/cinematch-preview.png.png)

**Discover your next favorite movie with CineMatch!*

CineMatch is a movie recommendation application built using Python and Streamlit. It helps users discover movies similar to their interests using a content-based filtering approach and movie metadata.

## 📌 Project Overview

CineMatch recommends movies based on a movie selected by the user. It uses TF-IDF vectorization and similarity calculations to identify movies with similar content.

The application provides a simple interface where users can search for movies and explore recommendations.

## ✨ Features

- 🎬 Movie recommendations based on selected movies
- 🔎 Movie search functionality
- 🎯 Content-based filtering
- 📊 TF-IDF text vectorization
- 🔗 Similarity-based movie matching
- 🖥️ Interactive Streamlit interface
- 🎨 User-friendly cinematic design
- 🎞️ Movie metadata integration
- 🌐 FastAPI backend integration, where configured

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Pandas | Data handling and preprocessing |
| NumPy | Numerical operations, if used |
| Scikit-learn | TF-IDF vectorization and similarity calculations |
| Streamlit | Frontend user interface |
| FastAPI | Backend API, if used |
| Pickle | Saving and loading preprocessed data and model artifacts |
| TMDB API | Movie information and images, if configured |
| Git and GitHub | Version control and project hosting |

## ⚙️ Recommendation Approach

CineMatch uses a content-based recommendation approach.

1. **Movie dataset:** Movie information is loaded from the prepared dataset.
2. **Text processing:** Relevant movie information is converted into numerical features.
3. **TF-IDF vectorization:** Text is represented using TF-IDF features.
4. **Similarity calculation:** Similarity scores are calculated between movies.
5. **Recommendation:** Movies with similar content are returned as recommendations.
6. **User interface:** Recommendations are presented through the Streamlit application.

## 📂 Project Structure

```text
CineMatch/
│
├── app.py
├── main.py
├── imdb_merged.csv
├── movies.pkl
├── indices.pkl
├── tfidf_matrix.pkl
├── requirements.txt
├── README.md
├── .gitignore
│
└── assets/
    └── cinematch-preview.png
```

*The files shown above should match the files included in your repository. Keep any additional files your application requires.*

## 🚀 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Nis-hanth/CineMatch.git
cd CineMatch
```

### 2. Create a Virtual Environment (Optional)

```bash
py -3.12 -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

If your project contains `requirements.txt`, run:

```bash
python -m pip install -r requirements.txt
```

If the file does not exist, install the packages required by your code.

### 4. Run the Streamlit Application

```bash
python -m streamlit run app.py
```

Streamlit will provide a local URL in the terminal, usually:

```text
http://localhost:8501
```

### 5. Run the FastAPI Backend (If Required)

If `main.py` contains a FastAPI application and the frontend depends on it, install FastAPI and Uvicorn if needed:

```bash
python -m pip install fastapi uvicorn
```

Then start the backend:

```bash
python -m uvicorn main:app --reload
```

The backend will usually be available at:

```text
http://127.0.0.1:8000
```

## ☁️ Deployment

The Streamlit frontend can be deployed using Streamlit Community Cloud.

1. Push the project to GitHub.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/).
3. Connect your GitHub account.
4. Select the `CineMatch` repository.
5. Select the `main` branch.
6. Set the main file path to `app.py`.
7. Configure required secrets and environment variables.
8. Deploy the application.

If the frontend uses a separately hosted FastAPI backend, ensure the backend is deployed and the frontend uses the correct backend URL.

## 🔐 Security

- Never commit `.env`, `api.txt`, or files containing API keys.
- Store API keys in environment variables or deployment secrets.
- If an API key has already been pushed to a public repository, revoke or rotate it.
- Avoid committing temporary files, virtual environments, and Python cache folders.

## 🎯 Project Objective

The objective of CineMatch is to make movie discovery easier by providing relevant recommendations based on movie content and similarity, through an accessible web interface.

## 👨‍💻 Author

**Nishant**

GitHub: [Nis-hanth](https://github.com/Nis-hanth)

---

*This README describes the intended project workflow. Actual features and dependencies depend on the code and configuration in the repository.*
