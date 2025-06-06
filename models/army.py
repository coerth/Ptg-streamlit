from pydantic import BaseModel, Field
from models.unit import Unit
from models.regiment import Regiment
from typing import List, Optional


class Army(BaseModel):
    name: str
    faction: str
    formation: Optional[str] = None
    points_limit: int
    points_used: int
    drops: int
    spell_lore: Optional[str] = None
    regiments: List[Regiment] = Field(default_factory=list)
    faction_terrain: Optional[str] = None