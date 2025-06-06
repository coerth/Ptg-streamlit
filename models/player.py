from pydantic import BaseModel
from bson import ObjectId
from models.army import Army


class Player(BaseModel):
    name: str
    army: Army
