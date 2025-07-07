import streamlit as st
import pandas as pd
import ast

# Load your dataset (make sure this file is in the same folder)
df = pd.read_csv("tmdb_5000_movies.csv")

# Convert genres from string to list if needed
if isinstance(df['genres'].iloc[0], str) and df['genres'].iloc[0].startswith("["):
    df['genres'] = df['genres'].apply(lambda x: [d['name'] for d in ast.literal_eval(x)])

# Streamlit UI
st.title("🎬 Movie Info Search Engine")

movie = st.text_input("Enter a movie name")

if movie:
    match = df[df['original_title'].str.contains(movie, case=False, na=False)]
    
    if not match.empty:
        m = match.iloc[0]
        st.subheader(f"🎬 {m['original_title']}")
        st.write(f"📅 **Release Date**: {m['release_date']}")
        st.write(f"🎭 **Genres**: {', '.join(m['genres']) if isinstance(m['genres'], list) else m['genres']}")
        st.write(f"⏱️ **Runtime**: {m['runtime']} minutes")
        st.write(f"⭐ **Rating**: {m['vote_average']} ({m['vote_count']} votes)")
     
    else:
        st.warning(f"❌ No movie found with name '{movie}'")
