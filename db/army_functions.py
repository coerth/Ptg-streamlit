from models.army import Army
from db.get_db import get_collection
from datetime import datetime
from bson import ObjectId

def set_player_army(army: Army, player_id: str):
    """
    Set or update the army for a player
    
    Args:
        army: The Army pydantic model
        player_id: ID of the player who owns this army
    
    Returns:
        True if successful, False otherwise
    """
    # Convert Pydantic model to dict for MongoDB
    army_dict = army.model_dump()
    
    # Add metadata
    army_dict["updated_at"] = datetime.now()
    
    # Convert string ID to ObjectId if needed
    if isinstance(player_id, str):
        try:
            player_id = ObjectId(player_id)
        except:
            pass
    
    # Update player document with the army data
    players_collection = get_collection("players")
    result = players_collection.update_one(
        {"_id": player_id},
        {"$set": {
            "army": army_dict,
            "last_updated": datetime.now()
        }}
    )
    
    return result.modified_count > 0

def get_player_army(player_id):
    """
    Get the army for a specific player
    
    Args:
        player_id: The ID of the player
    
    Returns:
        Army object or None if not found
    """
    players_collection = get_collection("players")
    
    # Convert string ID to ObjectId if needed
    if isinstance(player_id, str):
        try:
            player_id = ObjectId(player_id)
        except:
            pass
            
    # Find player document
    player = players_collection.find_one({"_id": player_id})
    
    if player and "army" in player:
        try:
            # Convert to Army object
            return Army.model_validate(player["army"])
        except Exception as e:
            print(f"Error converting army: {str(e)}")
    
    return None