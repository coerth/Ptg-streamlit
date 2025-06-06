import streamlit as st
from streamlit import session_state
from db.player_functions import get_all_players
from db.army_functions import set_player_army, get_player_army
from functions import parse_army_list

# Initialize session state for selected player
if 'selected_player' not in st.session_state:
    st.session_state.selected_player = None
if 'show_parser' not in st.session_state:
    st.session_state.show_parser = False
if 'view_army' not in st.session_state:
    st.session_state.view_army = None

# Function to select player and show parser
def select_player_for_army(player_id, player_name):
    st.session_state.selected_player = {'id': player_id, 'name': player_name}
    st.session_state.show_parser = True

# Main page content
st.title("Armies Management")
st.header("Player Armies")

# Show army details if viewing an army
if st.session_state.view_army:
    army = st.session_state.view_army
    
    # Back button
    if st.button("← Back to Player List"):
        st.session_state.view_army = None
        st.rerun()
    
    # Army details
    st.header(f"{army.faction}: {army.name}")
    
    # Display key stats in columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Points", f"{army.points_used}/{army.points_limit}")
    with col2:
        st.metric("Drops", army.drops)
    with col3:
        if army.spell_lore:
            st.metric("Spell Lore", army.spell_lore)
            
    # Display regiments and units (without nested expanders)
    st.subheader("Regiments and Units")
    for regiment in army.regiments:
        st.markdown(f"### {regiment.name}")
        for unit in regiment.units:
            unit_details = []
            if hasattr(unit, 'is_general') and unit.is_general:
                unit_details.append("🎖️ General")
            if hasattr(unit, 'reinforced') and unit.reinforced:
                unit_details.append("⚔️ Reinforced")
                
            details_str = " | ".join(unit_details) if unit_details else ""
            st.markdown(f"**{unit.name}** ({unit.points}pts) {details_str}")
            
            # Show additional unit details if available
            if hasattr(unit, 'command_traits') and unit.command_traits:
                st.write(f"Command Traits: {', '.join(unit.command_traits)}")
            if hasattr(unit, 'artefacts') and unit.artefacts:
                st.write(f"Artefacts: {', '.join(unit.artefacts)}")
            if hasattr(unit, 'notes') and unit.notes:
                for note in unit.notes:
                    st.write(f"• {note}")
            
            st.divider()

# Show army parser if a player is selected
elif st.session_state.show_parser and st.session_state.selected_player:
    player = st.session_state.selected_player
    
    st.subheader(f"Update Army for {player['name']}")
    
    # Check if player already has an army
    existing_army = get_player_army(player['id'])
    if existing_army:
        st.info(f"Current army: {existing_army.faction}: {existing_army.name}")
    
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
                
                # Save army to the player document
                success = set_player_army(army, player['id'])
                
                if success:
                    st.success(f"Army '{army.name}' saved successfully for {player['name']}!")
                    
                    # Display parsed army details
                    st.header(f"{army.faction}: {army.name}")
                    st.write(f"Points: {army.points_used}/{army.points_limit}")
                    st.write(f"Drops: {army.drops}")
                    
                    if army.spell_lore:
                        st.write(f"Spell Lore: {army.spell_lore}")
                    
                    # Option to return to list
                    if st.button("Return to Player List"):
                        st.session_state.show_parser = False
                        st.session_state.selected_player = None
                        st.rerun()
                else:
                    st.error("Failed to save army")
                    
            except Exception as e:
                st.error(f"Error parsing army list: {str(e)}")
        else:
            st.warning("Please paste an army list to parse.")
        
else:
    players = get_all_players()
    if players:
        for i, player in enumerate(players):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.subheader(f"Player: {player.name}")
                
                # Display army info if exists
                if hasattr(player, 'army') and player.army is not None:
                    if hasattr(player.army, 'name') and player.army.name:
                        st.write(f"Army: {player.army.name}")
                    if hasattr(player.army, 'faction') and player.army.faction:
                        st.write(f"Faction: {player.army.faction}")
                else:
                    st.write("No army assigned")
            
            with col2:
                # View button if player has army
                army = get_player_army(player.id)
                if army:
                    if st.button("View Army", key=f"view_{i}"):
                        # Store the army in session state instead of displaying immediately
                        st.session_state.view_army = army
                        st.rerun()
            
            with col3:
                # Determine if player has an army
                has_army = hasattr(player, 'army') and player.army is not None
                label = "Update Army" if has_army else "Add Army"
                
                st.button(label, key=f"update_{i}", 
                        on_click=select_player_for_army, 
                        args=(player.id, player.name))
                          
            st.divider()
    else:
        st.info("No players found. Add players to get started.")