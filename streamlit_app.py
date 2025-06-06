import streamlit as st
from db.get_db import get_collection
from db.player_functions import create_player
from datetime import datetime

st.set_page_config(
    page_title="Path to Glory",
    page_icon="🏆",
    layout="wide"
)

st.title("Path to Glory: Nerd Edition")
st.write("This is a placeholder for the Path to Glory: Nerd Edition app. "
         "Please check back later for updates or visit the main app page.")

players_collection = get_collection("players")

st.title("🛡️ Add New Player")

name = st.text_input("Player Name")

if st.button("Create Player"):
    if name:
        player_id = create_player(name)
        st.success(f"Player created with ID: {player_id}")
    else:
        st.warning("Please fill in all fields.")