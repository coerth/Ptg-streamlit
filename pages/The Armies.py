import streamlit as st
from state.army_page_state import init_session_state
from streamlit_modules.player.player_list import render_player_list
from streamlit_modules.army.army_view import render_army_view
from streamlit_modules.army.render_army_parser import render_army_parser

st.title("Armies Management")
st.header("Player Armies")

init_session_state()

def select_player_for_army(player_id, player_name):
    st.session_state.selected_player = {'id': player_id, 'name': player_name}
    st.session_state.show_parser = True

st.write("DEBUG: selected_player =", st.session_state.get("selected_player"))
st.write("DEBUG: view_army =", st.session_state.get("view_army"))
st.write("DEBUG: show_parser =", st.session_state.get("show_parser"))

if st.session_state.view_army and st.session_state.selected_player:
    render_army_view(st.session_state.selected_player)
elif st.session_state.show_parser and st.session_state.selected_player:
    render_army_parser(st.session_state.selected_player)
else:
    render_player_list(select_player_for_army)

