import streamlit as st
from streamlit_modules.batte_tracker import run_tracker

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

run_tracker()