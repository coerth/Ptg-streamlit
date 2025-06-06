import streamlit as st

def init_session_state():
    if 'selected_player' not in st.session_state:
        st.session_state.selected_player = None
    if 'show_parser' not in st.session_state:
        st.session_state.show_parser = False
    if 'view_army' not in st.session_state:
        st.session_state.view_army = None
