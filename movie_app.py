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
    "hotstar": ("Hotstar
