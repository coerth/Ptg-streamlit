from models import Army
from db.get_db import add_data_to_collection, get_collection
from datetime import datetime
from bson import ObjectId

def save_army(army: Army, player_id: str = None):
    """
    Save an army list to the database
    
    Args:
        army: The Army pydantic model
        player_id: Optional ID of the player who owns this army
    
    Returns:
        The ID of the inserted document
    """
    # Convert Pydantic model to dict for MongoDB
    army_dict = army.model_dump()
    
    # Add metadata
    army_dict["created_at"] = datetime.now()
    army_dict["updated_at"] = datetime.now()
    
    if player_id:
        # Convert string ID to ObjectId if needed
        if isinstance(player_id, str):
            try:
                player_id = ObjectId(player_id)
            except:
                pass
        army_dict["player_id"] = player_id
    
    # Save to MongoDB
    inserted_id = add_data_to_collection("armies", army_dict)
    return inserted_id

def get_armies_by_player(player_id):
    """
    Get all armies for a specific player
    
    Args:
        player_id: The ID of the player
    
    Returns:
        List of army documents
    """
    collection = get_collection("armies")
    
    # Convert string ID to ObjectId if needed
    if isinstance(player_id, str):
        try:
            player_id = ObjectId(player_id)
        except:
            pass
            
    armies = list(collection.find({"player_id": player_id}))
    return armies