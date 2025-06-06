from pydantic import BaseModel, Field
from models.army import Army
from typing import Optional
from pydantic import ConfigDict
from models.pyobjectid import PyObjectId
from bson import ObjectId

class Player(BaseModel):
    # Combined configuration using only model_config
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True
    )
    
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    name: Optional[str] = None
    army: Optional[Army] = None
    wins: int = 0
    losses: int = 0
    draws: int = 0
    played: int = 0