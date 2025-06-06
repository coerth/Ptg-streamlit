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

def get_player_by_id(players_collection: Collection, player_id: str) -> Optional[Player]:
    player_data = players_collection.find_one({"_id": player_id})
    if player_data:
        return Player(**player_data)
    return None

def get_all_players(players_collection: Collection) -> list[Player]:
    players = []
    for player_data in players_collection.find():
        players.append(Player(**player_data))
    return players