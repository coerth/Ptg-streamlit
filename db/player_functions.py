from pymongo.collection import Collection
from pydantic import BaseModel, Field
from typing import Optional
from models.player import Player
from models.army import Army

def create_player(players_collection: Collection, name: str, army_name: str, faction: str):
    new_player = Player(
        name=name,
        army=Army(name=army_name, faction=faction)
    )
    result = players_collection.insert_one(new_player.dict(by_alias=True))
    return str(result.inserted_id)