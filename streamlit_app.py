import streamlit as st
from db.get_db import add_data_to_collection
from datetime import datetime

st.set_page_config(
    page_title="Path to Glory",
    page_icon="🏆",
    layout="wide"
)

st.title("Path to Glory: Nerd Edition")
st.write("This is a placeholder for the Path to Glory: Nerd Edition app. "
         "Please check back later for updates or visit the main app page.")

if st.button("Add Example Data"):
    example_data = {
        "name": "Example Entry",
        "score": 100,
        "timestamp": datetime.now()
    }
    inserted_id = add_data_to_collection("my_collection", example_data)
    st.success(f"Data added successfully with ID: {inserted_id}")