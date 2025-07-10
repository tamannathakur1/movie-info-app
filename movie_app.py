import streamlit as st
import pandas as pd
import ast
import requests
import re

# 🔑 API KEYS
TMDB_API_KEY = "d75ba14a78f04afedfdd0836fb06d7e6"
RAPIDAPI_KEY = "40a0ec6ad8mshdf93d395ced8664p12f290jsnc4b651b07b25"

# ✅ Platform code to name + logo mapping
PLATFORM_LOGOS = {
    "netflix": ("Netflix", "https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg"),
    "prime": ("Amazon Prime Video", "https://upload.wikimedia.org/wikipedia/commons/f/f1/Prime_Video.png"),
    "disney": ("Disney+", "https://upload.wikimedia.org/wikipedia/commons/3/3e/Disney%2B_logo.svg"),
    "hotstar": ("Hotstar", "https://upload.wikimedia.org/wikipedia/commons/1/1e/Hotstar_logo.svg"),
    "hbo": ("HBO Max", "https://upload.wikimedia.org/wikipedia/commons/1/17/HBO_Max_Logo.svg"),
    "apple": ("Apple TV+", "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg"),
    "zee5": ("Zee5", "https://upload.wikimedia.org/wikipedia/commons/6/67/ZEE5_official_logo.png"),
    "sonyliv": ("SonyLIV", "https://upload.wikimedia.org/wikipedia/commons/b/b2/Sony_Liv_logo.svg"),
    "aha": ("Aha", "https://upload.wikimedia.org/wikipedia/commons/f/f4/Aha_OTT_Logo.png"),
    "jio": ("JioCinema", "https://upload.wikimedia.org/wikipedia/commons/0/0c/Jio_Cinema_Logo.png")
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

# ✅ Function to get streaming platforms
def get_streaming_providers(movie_title, country_code):
    cleaned_title = re.sub(r"[^\w\s]", "", movie_title).strip().lower()

    url = "https://streaming-availability.p.rapidapi.com/search/title"
    query = {
        "title": cleaned_title,
        "country": country_code,
        "show_type": "movie"
    }
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "streaming-availability.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=query)
        if response.status_code != 200:
            return []

        data = response.json()
        platforms = set()

        for item in data.get("result", []):
            info = item.get("streamingInfo", {}).get(country_code, {})
            for code in info.keys():
                if code in PLATFORM_LOGOS:
                    platforms.add(code)

        return sorted(platforms)

    except Exception as e:
        st.warning(f"⚠️ API Error: {e}")
        return []

# ✅ Load dataset
df = pd.read_csv("tmdb_5000_movies.csv")
if isinstance(df['genres'].iloc[0], str) and df['genres'].iloc[0].startswith("["):
    df['genres'] = df['genres'].apply(lambda x: [d['name'] for d in ast.literal_eva_]()
