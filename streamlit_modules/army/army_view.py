import streamlit as st

def render_army_view(army):
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
            if getattr(unit, 'command_traits', []):
                st.write(f"Command Traits: {', '.join(unit.command_traits)}")
            if getattr(unit, 'artefacts', []):
                st.write(f"Artefacts: {', '.join(unit.artefacts)}")
            if getattr(unit, 'notes', []):
                for note in unit.notes:
                    st.write(f"• {note}")
            st.divider()
