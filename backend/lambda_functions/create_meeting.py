from utils.mongo_service import client
        
def create_meeting(meeting_data, db=None):
    if db is None:
        db = client["cloudmeet"]
    return db["meetings"].insert_one(meeting_data).inserted_id
