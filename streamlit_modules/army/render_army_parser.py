import streamlit as st
from db.army_functions import get_player_army, set_player_army
from functions import parse_army_list

def render_army_parser(player):
    st.subheader(f"Update Army for {player['name']}")
    
    existing = get_player_army(player['id'])
    if existing:
        st.info(f"Current army: {existing.faction}: {existing.name}")
    
    if st.button("← Back to Player List"):
        st.session_state.show_parser = False
        st.session_state.selected_player = None
        st.rerun()
    
    army_text = st.text_area("Paste army list here:", height=300)
    
    if st.button("Parse and Save Army"):
        if not army_text:
            st.warning("Please paste an army list to parse.")
            return

        try:
            army = parse_army_list(army_text)
            success = set_player_army(army, player['id'])

            if success:
                st.success(f"Army '{army.name}' saved successfully for {player['name']}!")
                st.header(f"{army.faction}: {army.name}")
                st.write(f"Points: {army.points_used}/{army.points_limit}")
                st.write(f"Drops: {army.drops}")
                if army.spell_lore:
                    st.write(f"Spell Lore: {army.spell_lore}")
                if st.button("Return to Player List"):
                    st.session_state.show_parser = False
                    st.session_state.selected_player = None
                    st.rerun()
            else:
                st.error("Failed to save army")

        except Exception as e:
            st.error(f"Error parsing army list: {str(e)}")
