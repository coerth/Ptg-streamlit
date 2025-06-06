from pydantic import BaseModel, Field
from models.unit import Unit
from models.regiment import Regiment
from typing import List, Optional


class Army(BaseModel):
    name: Optional[str] = None
    faction: Optional[str] = None
    formation: Optional[str] = None
    points_limit: Optional[int] = 0
    points_used: Optional[int] = 0
    drops: Optional[int] = 0
    spell_lore: Optional[str] = None
    regiments: List[Regiment] = Field(default_factory=list)
    faction_terrain: Optional[str] = None