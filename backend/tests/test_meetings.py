import pytest
import mongomock
from lambda_functions.create_meeting import create_meeting

# Base MongoDB mockée
@pytest.fixture(scope="module")
def mock_db():
    client = mongomock.MongoClient()
    db = client["cloudmeet_test"]
    yield db  # simulation d'une base MongoDB
    client.drop_database("cloudmeet_test")

@pytest.fixture(autouse=True)
def clean_collection(mock_db):
    mock_db["meetings"].delete_many({})

def test_create_meeting_inserts_document(mock_db):
    meeting_data = {
        "title": "Réunion mockée",
        "datetime": "2025-08-01T10:00:00",
        "participants": ["mock@example.com"],
        "description": "Test avec mongomock",
        "user_id": "user_mock"
    }

    inserted_id = create_meeting(meeting_data, db=mock_db)
    meeting = mock_db["meetings"].find_one({"_id": inserted_id})

    # Test that document was inserted
    assert meeting is not None
    assert inserted_id is not None
    
    # Test all fields are correctly saved
    assert meeting["title"] == "Réunion mockée"
    assert meeting["datetime"] == "2025-08-01T10:00:00"
    assert meeting["participants"] == ["mock@example.com"]
    assert meeting["description"] == "Test avec mongomock"
    assert meeting["user_id"] == "user_mock"

def test_create_meeting_returns_valid_id(mock_db):
    """Test that create_meeting returns a valid ObjectId"""
    meeting_data = {
        "title": "Test Meeting",
        "user_id": "test_user"
    }
    
    inserted_id = create_meeting(meeting_data, db=mock_db)
    
    # Verify the ID is valid and the document exists
    assert inserted_id is not None
    assert mock_db["meetings"].find_one({"_id": inserted_id}) is not None

def test_create_meeting_with_minimal_data(mock_db):
    """Test creating a meeting with only required fields"""
    minimal_data = {
        "title": "Minimal Meeting"
    }
    
    inserted_id = create_meeting(minimal_data, db=mock_db)
    meeting = mock_db["meetings"].find_one({"_id": inserted_id})
    
    assert meeting is not None
    assert meeting["title"] == "Minimal Meeting"
