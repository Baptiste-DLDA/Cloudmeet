from utils.mongo_service import client
        
def create_meeting(meeting_data, db=None):
    """
    Create a new meeting in the database and return its ID.
    
    """
    if db is None:
        db = client["cloudmeet"]
    return db["meetings"].insert_one(meeting_data).inserted_id
