import streamlit as st
import pandas as pd
import ast
import requests

# Load your dataset
df = pd.read_csv("tmdb_5000_movies.csv")

# Convert genres from string to list if needed
if isinstance(df['genres'].iloc[0], str) and df['genres'].iloc[0].startswith("["):
    df['genres'] = df['genres'].apply(lambda x: [d['name'] for d in ast.literal_eval(x)])

# Set page title
st.set_page_config(page_title="Movie Info App", layout="centered")
st.title("🎬 Movie Info Search Engine")

# Dropdown for movie selection
movie_list = df['original_title'].dropna().unique()
selected_movie = st.selectbox("🔍 Select a movie title", sorted(movie_list))

# Filter all rows with the selected title (in case duplicates exist)
matches = df[df['original_title'] == selected_movie]

# Function to show poster (if using TMDB, replace with real URL logic)
def show_poster(poster_path):
    base_url = "https://image.tmdb.org/t/p/w500"
    if isinstance(poster_path, str) and poster_path != "":
        return base_url + poster_path
    else:
        return "https://via.placeholder.com/300x450?text=No+Poster"

# Show all matching entries
for i, m in matches.iterrows():
    st.markdown("---")
    st.subheader(f"🎬 {m['original_title']}")
    
    # Columns for layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Try showing poster image
        if 'poster_path' in m and pd.notna(m['poster_path']):
            poster_url = show_poster(m['poster_path'])
        else:
            poster_url = "https://via.placeholder.com/300x450?text=No+Poster"
        st.image(poster_url, width=250)

    with col2:
        st.write(f"📅 **Release Date**: {m['release_date']}")
        st.write(f"🎭 **Genres**: {', '.join(m['genres']) if isinstance(m['genres'], list) else m['genres']}")
        st.write(f"⏱️ **Runtime**: {m['runtime']} minutes")
        st.write(f"⭐ **Rating**: {m['vote_average']} ({m['vote_count']} votes)")
        st.markdown(f"📝 **Overview**: {m['overview']}")
