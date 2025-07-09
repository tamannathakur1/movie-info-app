import streamlit as st
import pandas as pd
import ast
import requests

# 🔑 API KEYS
TMDB_API_KEY = "d75ba14a78f04afedfdd0836fb06d7e6"
RAPIDAPI_KEY = "40a0ec6ad8mshdf93d395ced8664p12f290jsnc4b651b07b25"

# ✅ Platform code to readable name mapping
PLATFORM_MAP = {
    "netflix": "Netflix",
    "prime": "Amazon Prime Video",
    "disney": "Disney+",
    "hotstar": "Hotstar",
    "hbo": "HBO Max",
    "apple": "Apple TV+",
    "zee5": "Zee5",
    "sonyliv": "SonyLIV",
    "aha": "Aha",
    "jio": "JioCinema"
}

# ✅ Function to get poster from TMDB
def get_poster_url(movie_title):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": movie_title.strip()
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return "https://via.placeholder.com/300x450?text=Error"
    data = response.json()
    if data.get("results"):
        poster_path = data["results"][0].get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return "https://via.placeholder.com/300x450?text=No+Poster"

# ✅ Function to get streaming platforms using RapidAPI
def get_streaming_providers(movie_title):
    url = "https://streaming-availability.p.rapidapi.com/search/title"
    query = {
        "title": movie_title,
        "country": "IN",
        "show_type": "movie"
    }
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "streaming-availability.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=query)
    if response.status_code != 200:
        return ["Not Available"]

    data = response.json()
    platforms = set()

    for item in data.get("result", []):
        for code in item.get("streamingInfo", {}).get("in", {}).keys():
            platforms.add(PLATFORM_MAP.get(code, code.capitalize()))

    return sorted(platforms) if platforms else ["Not Available"]

# ✅ Load and process dataset
df = pd.read_csv("tmdb_5000_movies.csv")

# Clean genres column
if isinstance(df['genres'].iloc[0], str) and df['genres'].iloc[0].startswith("["):
    df['genres'] = df['genres'].apply(lambda x: [d['name'] for d in ast.literal_eval(x)])

# ✅ Streamlit UI
st.set_page_config(page_title="Movie Info App", layout="centered")
st.title("🎬 Movie Info Search Engine")

# Movie dropdown
movie_list = df['original_title'].dropna().unique()
selected_movie = st.selectbox("🔍 Select a movie title", sorted(movie_list))

# Show details
if selected_movie:
    movie_data = df[df['original_title'] == selected_movie].iloc[0]
    poster_url = get_poster_url(selected_movie)
    platforms = get_streaming_providers(selected_movie)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(poster_url, width=250)

    with col2:
        st.subheader(f"🎬 {movie_data['original_title']}")
        st.write(f"📅 **Release Date**: {movie_data['release_date']}")
        st.write(f"🎭 **Genres**: {', '.join(movie_data['genres']) if isinstance(movie_data['genres'], list) else movie_data['genres']}")
        st.write(f"⏱️ **Runtime**: {movie_data['runtime']} minutes")
        st.write(f"⭐ **Rating**: {movie_data['vote_average']} ({movie_data['vote_count']} votes)")
        st.write(f"📝 **Overview**: {movie_data['overview']}")
        st.write(f"📺 **Available On**: {', '.join(platforms)}")
