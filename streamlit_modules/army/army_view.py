import streamlit as st

def render_army_view(army):
    if "view_army" not in st.session_state or st.session_state.view_army != army:
        st.session_state.view_army = army
        st.rerun()

    army = st.session_state.view_army

    if st.button("← Back to Player List"):
        st.session_state.view_army = None
        st.rerun()

    st.header(f"{army.faction}: {army.name}")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Points", f"{army.points_used}/{army.points_limit}")
    with col2:
        st.metric("Drops", army.drops)
    with col3:
        if army.spell_lore:
            st.metric("Spell Lore", army.spell_lore)

    st.subheader("Regiments and Units")
    for regiment in army.regiments:
        st.markdown(f"### {regiment.name}")
        for unit in regiment.units:
            unit_details = []
            if getattr(unit, 'is_general', False):
                unit_details.append("🎖️ General")
            if getattr(unit, 'reinforced', False):
                unit_details.append("⚔️ Reinforced")
            details_str = " | ".join(unit_details)
            st.markdown(f"**{unit.name}** ({unit.points}pts) {details_str}")

            # Display new fields
            st.write(f"- **Size:** {getattr(unit, 'size', 'N/A')}")
            st.write(f"- **Path:** {getattr(unit, 'path', 'N/A') or 'None'}")
            st.write(f"- **Rank:** {getattr(unit, 'rank', 'N/A')}")
            st.write(f"- **Battle Wounds:** {getattr(unit, 'battle_wounds', 0)}")

            battle_scars = getattr(unit, 'battle_scars', [])
            if battle_scars:
                st.write("- **Battle Scars:**")
                for scar in battle_scars:
                    st.write(f"  • {scar}")
            else:
                st.write("- **Battle Scars:** None")

            # Existing fields
            if getattr(unit, 'command_traits', []):
                st.write(f"Command Traits: {', '.join(unit.command_traits)}")
            if getattr(unit, 'artefacts', []):
                st.write(f"Artefacts: {', '.join(unit.artefacts)}")
            if getattr(unit, 'notes', []):
                for note in unit.notes:
                    st.write(f"• {note}")

            st.divider()
