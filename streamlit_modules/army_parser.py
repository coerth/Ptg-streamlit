import streamlit as st
from functions import parse_army_list
import json

st.title("Army List Parser")

army_text = st.text_area("Paste your army list here:", height=300)

if st.button("Parse Army List"):
    if army_text:
        try:
            army = parse_army_list(army_text)
            st.success("Army list parsed successfully!")
            
            # Display army details
            st.header(f"{army.faction}: {army.name}")
            st.write(f"Points: {army.points_used}/{army.points_limit}")
            st.write(f"Drops: {army.drops}")
            
            if army.spell_lore:
                st.write(f"Spell Lore: {army.spell_lore}")
            
            # Display regiments and units
            for regiment in army.regiments:
                with st.expander(f"{regiment.name}"):
                    for unit in regiment.units:
                        unit_details = []
                        if unit.is_general:
                            unit_details.append("🎖️ General")
                        if unit.reinforced:
                            unit_details.append("⚔️ Reinforced")
                        if unit.command_traits:
                            unit_details.append(f"Command traits: {', '.join(unit.command_traits)}")
                        if unit.artefacts:
                            unit_details.append(f"Artefacts: {', '.join(unit.artefacts)}")
                            
                        details_str = " | ".join(unit_details) if unit_details else ""
                        st.write(f"**{unit.name}** ({unit.points}pts) {details_str}")
                        
                        if unit.notes:
                            for note in unit.notes:
                                st.write(f"- {note}")
            
            if army.faction_terrain:
                st.write(f"**Faction Terrain:** {army.faction_terrain}")
            
            # Option to view as JSON
            with st.expander("View as JSON"):
                st.code(army.model_dump_json(indent=2))
                
        except Exception as e:
            st.error(f"Error parsing army list: {str(e)}")
    else:
        st.warning("Please paste an army list to parse.")