from streamlit import page, session_state, session_state as st
from db.player_functions import get_all_players

st.widget("title", "The Armies")
st.widget("header", "List of Armies")
players = get_all_players()
if players:
    for player in players:
        st.widget("subheader", f"Player: {player['name']}")
        st.widget("markdown", f"- Army Name: **{player['army_name']}**")
        st.widget("markdown", f"- Faction: **{player['faction']}**")