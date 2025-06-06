import streamlit as st

def render_unit_editor(unit, regiment_index, unit_index):
    """
    Render editable inputs for a single unit and update the army in session state on changes.

    Args:
        unit: The UnitDetails object or dict representing the unit.
        regiment_index: Index of the regiment containing the unit (to identify it in the army).
        unit_index: Index of the unit within the regiment.
    """

    st.subheader(f"Edit Unit: {unit.name}")

    # Editable fields
    size = st.number_input("Size", min_value=1, value=getattr(unit, "size", 1), key=f"size_{regiment_index}_{unit_index}")
    reinforced = st.checkbox("Reinforced", value=getattr(unit, "reinforced", False), key=f"reinforced_{regiment_index}_{unit_index}")
    points = st.number_input("Points", min_value=0, value=getattr(unit, "points", 0), key=f"points_{regiment_index}_{unit_index}")
    battle_wounds = st.number_input("Battle Wounds", min_value=0, value=getattr(unit, "battle_wounds", 0), key=f"bw_{regiment_index}_{unit_index}")
    path = st.text_input("Path", value=getattr(unit, "path", ""), key=f"path_{regiment_index}_{unit_index}")
    rank = st.number_input("Rank", min_value=0, value=getattr(unit, "rank", 0), key=f"rank_{regiment_index}_{unit_index}")
    notes = st.text_area("Notes (comma separated)", value=", ".join(getattr(unit, "notes", [])), key=f"notes_{regiment_index}_{unit_index}")

    # Update the unit object in the army stored in session state when user clicks "Save"
    if st.button("Save Changes", key=f"save_{regiment_index}_{unit_index}"):
        # Update attributes
        unit.size = size
        unit.battle_wounds = battle_wounds
        unit.notes = [note.strip() for note in notes.split(",") if note.strip()]
        unit.reinforced = reinforced
        unit.path = path
        unit.rank = rank
        unit.points = points

        # Update army in session state
        army = st.session_state.view_army
        army.regiments[regiment_index].units[unit_index] = unit
        st.session_state.view_army = army

        st.success(f"Updated unit '{unit.name}' successfully.")
        st.experimental_rerun()
