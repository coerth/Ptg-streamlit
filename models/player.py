from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from models.pyobjectid import PyObjectId
from models.army import Army


class Player(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    army: Army

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}