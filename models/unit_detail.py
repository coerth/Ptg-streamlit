from pydantic import BaseModel, Field
from typing import List, Optional
from .unit import Unit

class UnitDetails(Unit):
    is_general: bool = False
    command_traits: List[str] = Field(default_factory=list)
    artefacts: List[str] = Field(default_factory=list)
    reinforced: bool = False
    notes: List[str] = Field(default_factory=list)