import streamlit as st
from streamlit import session_state
from db.player_functions import get_all_players

st.title("Armies Overview")
st.header("List of All Players and Their Armies")
players = get_all_players()
if players:
    for player in players:
        st.subheader(f"Player: {player.name}")
        st.markdown(f"- Army Name: **{player.army.name}**")
        st.markdown(f"- Faction: **{player.army.faction}**")