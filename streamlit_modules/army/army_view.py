import streamlit as st
from functions.parse_army import parse_army_list
from db.army_functions import get_player_army, set_player_army
from functions import parse_army_list

def render_army_view(player):
    if st.session_state.get("view_army_reload", False) or "view_army" not in st.session_state:
        army = get_player_army(player['id'])
        st.session_state.view_army = army
        st.session_state.view_army_reload = False
        st.rerun()

    army = st.session_state.view_army

    st.write(player)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Player List"):
            st.session_state.view_army = None
            st.session_state.selected_player = None
            st.session_state.show_overwrite_form = False
            st.rerun()
    
    if not st.session_state.get("show_overwrite_form", False):
        with col2:
            if st.button("🔄 Reload Army From Clipboard"):
                st.session_state.show_overwrite_form = True
                st.rerun()
        
        st.header(f"{army.faction}: {army.name}")
        st.metric("Points", f"{army.points_used}/{army.points_limit}")
        st.metric("Drops", army.drops)
        if army.spell_lore:
            st.metric("Spell Lore", army.spell_lore)

        st.subheader("Regiments and Units")
        for regiment in army.regiments:
            st.markdown(f"### {regiment.name}")
            for unit in regiment.units:
                st.markdown(f"**{unit.name}** ({unit.points}pts)")
                st.write(f"- Size: {getattr(unit, 'size', 'N/A')}")
                st.write(f"- Path: {getattr(unit, 'path', 'N/A')}")
                st.write(f"- Rank: {getattr(unit, 'rank', 'N/A')}")
                st.write(f"- Battle Wounds: {getattr(unit, 'battle_wounds', 0)}")
                if getattr(unit, 'battle_scars', []):
                    st.write("- Battle Scars:")
                    for scar in unit.battle_scars:
                        st.write(f"  • {scar}")
                if getattr(unit, 'command_traits', []):
                    st.write(f"Command Traits: {', '.join(unit.command_traits)}")
                if getattr(unit, 'artefacts', []):
                    st.write(f"Artefacts: {', '.join(unit.artefacts)}")
                if getattr(unit, 'notes', []):
                    for note in unit.notes:
                        st.write(f"• {note}")
                st.divider()
    else:
        st.header("Update Army List")
        st.write(f"Overwriting army for player: {player['name']}")
        
        if st.button("Cancel Update"):
            st.session_state.show_overwrite_form = False
            st.rerun()
            
        army_text = st.text_area("Paste new army list here:", height=300, key="army_text")

        if st.button("Parse and Overwrite Army"):
            if not army_text.strip():
                st.warning("Please paste an army list first.")
            else:
                try:

                    
                    
                    parsed_army = parse_army_list(army_text)
                    
                    player_id = player['id']
                    success = set_player_army(parsed_army, player_id)
                    
                    if success:

                        st.session_state.view_army = parsed_army
                        st.success(f"Army '{parsed_army.name}' saved successfully!")
                        st.session_state.show_overwrite_form = False
                        st.rerun()
                    else:
                        st.error("Failed to save the army")
                        
                except Exception as e:
                    st.error(f"Parsing error: {str(e)}")
                    st.exception(e) 