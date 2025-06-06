import streamlit as st
from streamlit import session_state
from db.player_functions import get_all_players
from functions import parse_army_list
from db.army_functions import save_army

# Initialize session state for selected player
if 'selected_player' not in st.session_state:
    st.session_state.selected_player = None
if 'show_parser' not in st.session_state:
    st.session_state.show_parser = False

# Function to select player and show parser
def select_player_for_army(player_id, player_name):
    st.session_state.selected_player = {'id': player_id, 'name': player_name}
    st.session_state.show_parser = True

# Main page content
st.title("Armies Overview")
st.header("List of All Players and Their Armies")

# Show army parser if a player is selected
if st.session_state.show_parser and st.session_state.selected_player:
    player = st.session_state.selected_player
    
    st.subheader(f"Add Army for {player['name']}")
    
    # Back button
    if st.button("← Back to Player List"):
        st.session_state.show_parser = False
        st.session_state.selected_player = None
        st.rerun()
    
    # Army parser
    army_text = st.text_area("Paste army list here:", height=300)
    
    if st.button("Parse and Save Army"):
        if army_text:
            try:
                army = parse_army_list(army_text)
                
                # Save army with player association
                inserted_id = save_army(army, player['id'])
                st.success(f"Army '{army.name}' saved successfully for {player['name']}!")
                
                # Display parsed army details
                st.write(f"**{army.faction}: {army.name}**")
                st.write(f"Points: {army.points_used}/{army.points_limit}")
                
                # Option to add another or return to list
                if st.button("Add Another Army"):
                    st.rerun()
                if st.button("Return to Player List"):
                    st.session_state.show_parser = False
                    st.session_state.selected_player = None
                    st.rerun()
                    
            except Exception as e:
                st.error(f"Error parsing army list: {str(e)}")
        else:
            st.warning("Please paste an army list to parse.")
        
# Display player list when not showing parser
else:
    players = get_all_players()
    if players:
        for player in players:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.subheader(f"Player: {player.name}")
            with col2:
                st.button("Add Army", key=f"add_army_{player.id}", 
                          on_click=select_player_for_army, 
                          args=(player.id, player.name))
                          
            st.divider()
    else:
        st.info("No players found. Add players to get started.")