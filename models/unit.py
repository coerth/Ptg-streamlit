from pydantic import BaseModel, Field
from typing import List, Optional

class Unit(BaseModel):
    name: Optional[str] = None
    size: Optional[int] = 1
    path: Optional[str] = None
    rank: Optional[int] = 0
    abilities: List[str] = Field(default_factory=list)
    enchantments: List[str] = Field(default_factory=list)
    battle_wounds: Optional[int] = 0
    battle_scars: List[str] = Field(default_factory=list)
    points: Optional[int] = 0