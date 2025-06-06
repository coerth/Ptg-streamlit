from pydantic import BaseModel, Field
from typing import List
from models.unit_detail import UnitDetails

class Regiment(BaseModel):
    name: str
    units: List[UnitDetails] = Field(default_factory=list)