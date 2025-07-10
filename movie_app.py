import streamlit as st
import pandas as pd
import ast
import requests

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

# ✅ Function to get streaming platforms with logos
def get_streaming_providers(movie_title):
    country_code = "us"
    url = "https://streaming-availability.p.rapidapi.com/search/title"
    query = {
        "title": movie_title,
        "country": country_code.upper(),
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
            streaming_info = item.get("streamingInfo", {}).get(country_code, {})
            for code in streaming_info.keys():
                if code in PLATFORM_LOGOS:
                    platforms.add(code)

        return sorted(platforms)

    except Exception as e:
        return []

# ✅ Function to get YouTube trailer link
def get_trailer_youtube_link(movie_title):
    query = movie_title.replace(" ", "+") + "+official+trailer"
    return f"https://www.youtube.com/results?search_query={query}"

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
    platform_codes = get_streaming_providers(selected_movie)

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

        st.markdown("📺 **Available On:**")
        if platform_codes:
            for code in platform_codes:
                name, logo = PLATFORM_LOGOS[code]
                st.markdown(f"<img src='{logo}' alt='{name}' width='100'>", unsafe_allow_html=True)
        else:
            st.write("Not Available")

        # 🎞️ Trailer Section
        trailer_url = get_trailer_youtube_link(selected_movie)
        st.markdown("🎬 **Watch Trailer**")
        st.markdown(f"[▶️ Click here to watch on YouTube]({trailer_url})", unsafe_allow_html=True)
