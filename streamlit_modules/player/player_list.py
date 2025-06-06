import streamlit as st
from db.player_functions import get_all_players
from db.army_functions import get_player_army

def render_player_list(select_player_callback):
    players = get_all_players()
    
    if not players:
        st.info("No players found. Add players to get started.")
        return
    
    for i, player in enumerate(players):
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.subheader(f"Player: {player.name}")
            army = getattr(player, 'army', None)
            if army:
                st.write(f"Army: {army.name}")
                st.write(f"Faction: {army.faction}")
            else:
                st.write("No army assigned")
        
        with col2:
            army = get_player_army(player.id)
            if army:
                if st.button("View Army", key=f"view_{i}"):
                    st.session_state.view_army = army
                    st.rerun()
        
        with col3:
            label = "Update Army" if getattr(player, 'army', None) else "Add Army"
            st.button(label, key=f"update_{i}",
                      on_click=select_player_callback,
                      args=(player.id, player.name))
        
        st.divider()
