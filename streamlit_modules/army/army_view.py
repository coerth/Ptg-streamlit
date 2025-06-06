import streamlit as st
from functions.parse_army import parse_army_list
from db.army_functions import get_player_army, set_player_army

def render_army_view(player):
    if not player or not isinstance(player, dict) or "name" not in player:
        st.error("Invalid player data. Please return to the player list.")
        return

    if st.session_state.get("view_army_reload", False) or "view_army" not in st.session_state:
        army = get_player_army(player['id'])
        st.session_state.view_army = army
        st.session_state.view_army_reload = False
        st.rerun()

    army = st.session_state.view_army

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

        with st.form("unit_edit_form"):
            for reg_idx, regiment in enumerate(army.regiments):
                st.markdown(f"### {regiment.name}")
                for unit_idx, unit in enumerate(regiment.units):
                    with st.expander(f"⚔️ {unit.name} ({unit.points} pts)"):
                        size = st.number_input(
                            f"Size ({unit.name})", min_value=1, value=getattr(unit, 'size', 1),
                            key=f"size_{reg_idx}_{unit_idx}"
                        )
                        points = st.number_input(
                            f"Points ({unit.name})", min_value=0, value=getattr(unit, 'points', 0),
                            key=f"points_{reg_idx}_{unit_idx}"
                        )
                        path = st.text_input(
                            f"Path ({unit.name})", value=getattr(unit, 'path', ''),
                            key=f"path_{reg_idx}_{unit_idx}"
                        )
                        rank = st.text_input(
                            f"Rank ({unit.name})", value=getattr(unit, 'rank', ''),
                            key=f"rank_{reg_idx}_{unit_idx}"
                        )
                        battle_wounds = st.number_input(
                            f"Battle Wounds ({unit.name})", min_value=0,
                            value=getattr(unit, 'battle_wounds', 0),
                            key=f"wounds_{reg_idx}_{unit_idx}"
                        )
                        reinforced = st.checkbox(
                            f"Reinforced ({unit.name})", value=getattr(unit, 'reinforced', False),
                            key=f"reinforced_{reg_idx}_{unit_idx}"
                        )

                        # Store updated values in session state
                        st.session_state[f"unit_{reg_idx}_{unit_idx}"] = {
                            "size": size,
                            "points": points,
                            "path": path,
                            "rank": rank,
                            "battle_wounds": battle_wounds,
                            "reinforced": reinforced,
                        }

                        if getattr(unit, 'battle_scars', []):
                            st.markdown("**Battle Scars**")
                            for scar in unit.battle_scars:
                                st.write(f"• {scar}")

                        if getattr(unit, 'command_traits', []):
                            st.write(f"Command Traits: {', '.join(unit.command_traits)}")
                        if getattr(unit, 'artefacts', []):
                            st.write(f"Artefacts: {', '.join(unit.artefacts)}")
                        if getattr(unit, 'notes', []):
                            for note in unit.notes:
                                st.write(f"• {note}")
                    st.divider()

            submitted = st.form_submit_button("💾 Save Unit Changes")
            if submitted:
                for reg_idx, regiment in enumerate(army.regiments):
                    for unit_idx, unit in enumerate(regiment.units):
                        key = f"unit_{reg_idx}_{unit_idx}"
                        if key in st.session_state:
                            values = st.session_state[key]
                            unit.size = values["size"]
                            unit.points = values["points"]
                            unit.path = values["path"]
                            unit.rank = values["rank"]
                            unit.battle_wounds = values["battle_wounds"]
                            unit.reinforced = values["reinforced"]

                success = set_player_army(army, player['id'])
                if success:
                    st.success("Army updated with new unit values!")
                else:
                    st.error("Failed to update the army.")
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
