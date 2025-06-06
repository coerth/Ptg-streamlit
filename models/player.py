from pydantic import BaseModel
from bson import ObjectId
from models.army import Army
from typing import Optional



class Player(BaseModel):
    id: Optional[ObjectId] = None
    name: Optional[str] = None
    army: Optional[Army] = None
    wins: int = 0
    losses: int = 0
    draws: int = 0
    played: int = 0
