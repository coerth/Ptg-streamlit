from models import Army
from db.get_db import get_collection
from datetime import datetime
from bson import ObjectId

def add_army_to_player(army: Army, player_id: str):
    """
    Add an army to a player document by embedding it
    
    Args:
        army: The Army pydantic model
        player_id: ID of the player who owns this army
    
    Returns:
        True if successful, False otherwise
    """
    # Convert army to dict for MongoDB
    army_dict = army.model_dump()
    
    # Add metadata
    army_dict["created_at"] = datetime.now()
    army_dict["updated_at"] = datetime.now()
    # Generate a unique ID for the army within the player document
    army_dict["id"] = str(ObjectId())
    
    # Get players collection
    players_collection = get_collection("players")
    
    # Convert string ID to ObjectId if needed
    if isinstance(player_id, str):
        try:
            player_id = ObjectId(player_id)
        except:
            pass
    
    # Update player document to add the army
    result = players_collection.update_one(
        {"_id": player_id},
        {"$push": {"armies": army_dict}}
    )
    
    return result.modified_count > 0

def get_player_armies(player_id):
    """
    Get all armies for a specific player
    
    Args:
        player_id: The ID of the player
    
    Returns:
        List of army objects
    """
    players_collection = get_collection("players")
    
    # Convert string ID to ObjectId if needed
    if isinstance(player_id, str):
        try:
            player_id = ObjectId(player_id)
        except:
            pass
    
    # Find the player
    player = players_collection.find_one({"_id": player_id})
    
    if player and "armies" in player:
        # Convert dictionaries to Army objects if needed
        return player["armies"]
    return []

def get_player_army(player_id, army_id):
    """
    Get a specific army from a player
    
    Args:
        player_id: The ID of the player
        army_id: The ID of the army
    
    Returns:
        Army object or None if not found
    """
    players_collection = get_collection("players")
    
    # Convert IDs to ObjectId if needed
    if isinstance(player_id, str):
        try:
            player_id = ObjectId(player_id)
        except:
            pass
            
    # Find player and extract the specific army
    player = players_collection.find_one(
        {"_id": player_id, "armies.id": army_id},
        {"armies.$": 1}
    )
    
    if player and "armies" in player and len(player["armies"]) > 0:
        return player["armies"][0]
    return None