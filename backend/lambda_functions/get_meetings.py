from utils.mongo_service import client
from typing import List, Dict, Any, Optional


def get_meetings_by_user_id(user_id: str, db=None) -> List[Dict[str, Any]]:
    """
    Fetch all meetings for a specific user.
    
    Args:
        user_id (str): The user ID to search for
        db: Optional database connection (for testing)
    
    Returns:
        List[Dict[str, Any]]: List of meeting documents for the user
    """
    if db is None:
        db = client["cloudmeet"]
    
    try:
        # Find all meetings where user_id matches
        meetings_cursor = db["meetings"].find({"user_id": user_id})
        meetings = list(meetings_cursor)
        
        # Convert ObjectId to string for JSON serialization
        for meeting in meetings:
            if "_id" in meeting:
                meeting["_id"] = str(meeting["_id"])
        
        return meetings
    
    except Exception as e:
        print(f"Error fetching meetings for user {user_id}: {str(e)}")
        return []


def get_meeting_by_id(meeting_id: str, db=None) -> Optional[Dict[str, Any]]:
    """
    Fetch a specific meeting by its ID.
    
    Args:
        meeting_id (str): The meeting ID to search for
        db: Optional database connection (for testing)
    
    Returns:
        Optional[Dict[str, Any]]: Meeting document if found, None otherwise
    """
    if db is None:
        db = client["cloudmeet"]
    
    try:
        from bson import ObjectId
        
        # Convert string ID to ObjectId for MongoDB query
        object_id = ObjectId(meeting_id)
        meeting = db["meetings"].find_one({"_id": object_id})
        
        if meeting:
            # Convert ObjectId to string for JSON serialization
            meeting["_id"] = str(meeting["_id"])
        
        return meeting
    
    except Exception as e:
        print(f"Error fetching meeting {meeting_id}: {str(e)}")
        return None


def get_all_meetings(db=None) -> List[Dict[str, Any]]:
    """
    Fetch all meetings from the database.
    
    Args:
        db: Optional database connection (for testing)
    
    Returns:
        List[Dict[str, Any]]: List of all meeting documents
    """
    if db is None:
        db = client["cloudmeet"]
    
    try:
        meetings_cursor = db["meetings"].find()
        meetings = list(meetings_cursor)
        
        # Convert ObjectId to string for JSON serialization
        for meeting in meetings:
            if "_id" in meeting:
                meeting["_id"] = str(meeting["_id"])
        
        return meetings
    
    except Exception as e:
        print(f"Error fetching all meetings: {str(e)}")
        return []


def delete_meeting_by_id(meeting_id: str, db=None) -> bool:
    """
    Delete a specific meeting by its ID.
    
    Args:
        meeting_id (str): The meeting ID to delete
        db: Optional database connection (for testing)
    
    Returns:
        bool: True if meeting was deleted successfully, False otherwise
    """
    if db is None:
        db = client["cloudmeet"]
    
    try:
        from bson import ObjectId
        
        # Convert string ID to ObjectId for MongoDB query
        object_id = ObjectId(meeting_id)
        result = db["meetings"].delete_one({"_id": object_id})
        
        return result.deleted_count > 0
    
    except Exception as e:
        print(f"Error deleting meeting {meeting_id}: {str(e)}")
        return False


def delete_meetings_by_user_id(user_id: str, db=None) -> int:
    """
    Delete all meetings for a specific user.
    
    Args:
        user_id (str): The user ID whose meetings should be deleted
        db: Optional database connection (for testing)
    
    Returns:
        int: Number of meetings deleted
    """
    if db is None:
        db = client["cloudmeet"]
    
    try:
        result = db["meetings"].delete_many({"user_id": user_id})
        return result.deleted_count
    
    except Exception as e:
        print(f"Error deleting meetings for user {user_id}: {str(e)}")
        return 0


def delete_all_meetings(db=None) -> int:
    """
    Delete all meetings from the database.
    WARNING: This operation cannot be undone!
    
    Args:
        db: Optional database connection (for testing)
    
    Returns:
        int: Number of meetings deleted
    """
    if db is None:
        db = client["cloudmeet"]
    
    try:
        result = db["meetings"].delete_many({})
        return result.deleted_count
    
    except Exception as e:
        print(f"Error deleting all meetings: {str(e)}")
        return 0
