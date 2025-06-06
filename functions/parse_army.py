import re
from models import Army, Regiment, UnitDetails

def parse_army_list(text: str) -> Army:
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Extract basic army info
    points_match = re.search(r'PtG (\d+)/(\d+) pts', text)
    points_used = int(points_match.group(1)) if points_match else 0
    points_limit = int(points_match.group(2)) if points_match else 0
    
    faction_name_match = re.match(r'(.+) \| (.+)', lines[1])
    faction = faction_name_match.group(1) if faction_name_match else "Unknown"
    army_name = faction_name_match.group(2) if faction_name_match else "Unknown"
    
    drops_match = re.search(r'Drops: (\d+)', text)
    drops = int(drops_match.group(1)) if drops_match else 0
    
    spell_lore = None
    if "Spell Lore" in text:
        spell_lore_line = [l for l in lines if "Spell Lore" in l][0]
        spell_lore = spell_lore_line.split("- ")[1] if "- " in spell_lore_line else None
    
    # Create army object
    army = Army(
        name=army_name,
        faction=faction,
        points_limit=points_limit,
        points_used=points_used,
        drops=drops,
        spell_lore=spell_lore,
        regiments=[]
    )
    
    # Parse regiments and units
    current_regiment = None
    current_unit = None
    
    for line in lines:
        # Regiment identification
        if "Regiment" in line or "General's Regiment" in line:
            if current_regiment:
                army.regiments.append(current_regiment)
            current_regiment = Regiment(name=line.strip())
            continue
            
        # Faction terrain
        if "Faction Terrain" in line:
            # Get the next line as the terrain name
            terrain_index = lines.index(line)
            if terrain_index + 1 < len(lines):
                army.faction_terrain = lines[terrain_index + 1]
            continue
            
        # Unit identification (has points)
        points_match = re.search(r'\((\d+)\)', line)
        if points_match:
            unit_name = line.split("(")[0].strip()
            points = int(points_match.group(1))
            
            current_unit = UnitDetails(
                name=unit_name,
                size=1,  # Default, update if we can parse this
                path="",  # Would need to be determined separately
                rank=1,   # Default, update if we can parse this
                abilities=[],
                enchantments=[],
                battle_wounds=0,
                battle_svars=[],
                points=points
            )
            
            if current_regiment:
                current_regiment.units.append(current_unit)
            continue
            
        # Unit details (bullet points)
        if line.startswith('•') or line.startswith(' •'):
            detail = line.replace('•', '').strip()
            
            if current_unit:
                if "General" in detail:
                    current_unit.is_general = True
                elif "Reinforced" in detail:
                    current_unit.reinforced = True
                # Try to categorize other bullet points
                elif detail in ["Cloaked in Shadow"]:  # Known command traits
                    current_unit.command_traits.append(detail)
                elif detail in ["Lightshard of the Harvest Moon"]:  # Known artifacts
                    current_unit.artefacts.append(detail)
                else:
                    current_unit.notes.append(detail)
    
    # Add the last regiment if it exists
    if current_regiment and current_regiment not in army.regiments:
        army.regiments.append(current_regiment)
    
    return army