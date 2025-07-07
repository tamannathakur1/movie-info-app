import streamlit as st
import pandas as pd
import ast
import requests

# 🔑 TMDB API Key
TMDB_API_KEY = "d75ba14a78f04afedfdd0836fb06d7e6"

# Function to get poster URL
def get_poster_url(movie_title):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": movie_title
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data["results"]:
        poster_path = data["results"][0].get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return "https://via.placeholder.com/300x450?text=No+Poster+Available"

# Load dataset
df = pd.read_csv("tmdb_5000_movies.csv")

# Convert genres from string to list
if isinstance(df['genres'].iloc[0], str) and df['genres'].iloc[0].startswith("["):
    df['genres'] = df['genres'].apply(lambda x: [d['name'] for d in ast.literal_eval(x)])

# Streamlit UI
st.set_page_config(page_title="Movie Info App", layout="centered")
st.title("🎬 Movie Info Search Engine")

# Dropdown of all movies
movie_list = df['original_title'].dropna().unique()
selected_movie = st.selectbox("🔍 Select a movie", sorted(movie_list))

# Show movie info
if selected_movie:
    movie_data = df[df['original_title'] == selected_movie].iloc[0]

    col1, col2 = st.columns([1, 2])

    with col1:
        poster_url = get_poster_url(selected_movie)
        st.image(poster_url, width=250)

    with col2:
        st.markdown(f"### 🎬 {movie_data['original_title']}")
        st.write(f"📅 **Release Date**: {movie_data['release_date']}")
        st.write(f"🎭 **Genres**: {', '.join(movie_data['genres']) if isinstance(movie_data['genres'], list) else movie_data['genres']}")
        st.write(f"⏱️ **Runtime**: {movie_data['runtime']} minutes")
        st.write(f"⭐ **Rating**: {movie_data['vote_average']} ({movie_data['vote_count']} votes)")
        st.write(f"📝 **Overview**: {movie_data['overview']}")
