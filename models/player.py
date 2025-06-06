from pydantic import BaseModel
from bson import ObjectId
from models.army import Army
from typing import Optional
from pydantic import ConfigDict
from models.pyobjectid import PyObjectId



class Player(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    id: Optional[PyObjectId] = None
    name: Optional[str] = None
    army: Optional[Army] = None
    wins: int = 0
    losses: int = 0
    draws: int = 0
    played: int = 0

    class Config:
        populate_by_name = True