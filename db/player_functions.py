from pymongo.collection import Collection
from pydantic import BaseModel, Field
from typing import Optional
from models.player import Player
from models.army import Army
from db.get_db import get_collection

def create_player(players_collection: Collection, name: str):
    new_player = Player(
        name=name
    )
    result = players_collection.insert_one(new_player.dict(by_alias=True))
    return str(result.inserted_id)

def get_player_by_id(players_collection: Collection, player_id: str) -> Optional[Player]:
    player_data = players_collection.find_one({"_id": player_id})
    if player_data:
        return Player(**player_data)
    return None

def get_all_players() -> list[Player]:
    players_collection = get_collection("players")
    if players_collection is None:
        return []
    
    players = []
    for player_data in players_collection.find():
        players.append(Player(**player_data))
    return players