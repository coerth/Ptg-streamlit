from models.player import Player
from db.get_db import get_collection, add_data_to_collection
from bson import ObjectId
from typing import List

def create_player(player_data: dict):
    """
    Create a new player in the database
    """
    collection = get_collection("players")
    player_id = add_data_to_collection("players", player_data)
    return player_id

def get_player(player_id):
    """
    Get a player by ID
    """
    collection = get_collection("players")
    if isinstance(player_id, str):
        player_id = ObjectId(player_id)
    player_data = collection.find_one({"_id": player_id})
    if player_data:
        # Convert ObjectId to string for Pydantic
        player_data["_id"] = str(player_data["_id"])
        return Player(**player_data)
    return None

def get_all_players() -> List[Player]:
    """
    Get all players
    """
    collection = get_collection("players")
    players = []
    
    for player_data in collection.find():
        # Convert ObjectId to string for Pydantic
        player_data["_id"] = str(player_data["_id"])
        players.append(Player(**player_data))
    
    return players