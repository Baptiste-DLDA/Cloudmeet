#!/usr/bin/env python3
"""
Unit tests for the get_meetings functionality using pytest.
"""

import pytest
import mongomock
from lambda_functions.get_meetings import (
    get_meetings_by_user_id, 
    get_meeting_by_id, 
    get_all_meetings,
    delete_meeting_by_id,
    delete_meetings_by_user_id,
    delete_all_meetings
)
from lambda_functions.create_meeting import create_meeting


# Base MongoDB mockée
@pytest.fixture(scope="module")
def mock_db():
    """Create a mock MongoDB database for testing."""
    client = mongomock.MongoClient()
    db = client["cloudmeet_test"]
    yield db
    client.drop_database("cloudmeet_test")


@pytest.fixture(autouse=True)
def clean_collection(mock_db):
    """Clean the meetings collection before each test."""
    mock_db["meetings"].delete_many({})


@pytest.fixture
def sample_meetings_data():
    """Sample meeting data for testing."""
    return [
        {
            "title": "Team Standup",
            "datetime": "2025-07-25T09:00:00",
            "participants": ["user@example.com", "teammate@example.com"],
            "description": "Daily team standup meeting",
            "user_id": "test_user_1"
        },
        {
            "title": "Project Review",
            "datetime": "2025-07-25T14:00:00",
            "participants": ["user@example.com", "manager@example.com"],
            "description": "Monthly project review",
            "user_id": "test_user_1"
        },
        {
            "title": "Client Meeting",
            "datetime": "2025-07-26T10:00:00",
            "participants": ["client@company.com"],
            "description": "Meeting with client",
            "user_id": "test_user_2"
        }
    ]


@pytest.fixture
def created_meetings(mock_db, sample_meetings_data):
    """Create sample meetings and return their IDs."""
    meeting_ids = []
    for meeting_data in sample_meetings_data:
        meeting_id = create_meeting(meeting_data, db=mock_db)
        meeting_ids.append(meeting_id)
    return meeting_ids


# Tests for get_meetings_by_user_id
class TestGetMeetingsByUserId:
    
    def test_get_meetings_by_user_id_returns_correct_meetings(self, mock_db, created_meetings, sample_meetings_data):
        """Test that get_meetings_by_user_id returns correct meetings for a user."""
        meetings = get_meetings_by_user_id("test_user_1", db=mock_db)
        
        assert len(meetings) == 2
        assert all(meeting["user_id"] == "test_user_1" for meeting in meetings)
        
        # Check meeting titles
        meeting_titles = [meeting["title"] for meeting in meetings]
        assert "Team Standup" in meeting_titles
        assert "Project Review" in meeting_titles
    
    def test_get_meetings_by_user_id_single_meeting(self, mock_db, created_meetings):
        """Test getting meetings for user with single meeting."""
        meetings = get_meetings_by_user_id("test_user_2", db=mock_db)
        
        assert len(meetings) == 1
        assert meetings[0]["user_id"] == "test_user_2"
        assert meetings[0]["title"] == "Client Meeting"
    
    def test_get_meetings_by_user_id_no_meetings(self, mock_db, created_meetings):
        """Test getting meetings for user with no meetings."""
        meetings = get_meetings_by_user_id("non_existent_user", db=mock_db)
        
        assert len(meetings) == 0
        assert meetings == []
    
    def test_get_meetings_by_user_id_empty_database(self, mock_db):
        """Test getting meetings when database is empty."""
        meetings = get_meetings_by_user_id("any_user", db=mock_db)
        
        assert len(meetings) == 0
        assert meetings == []
    
    def test_get_meetings_by_user_id_converts_object_id_to_string(self, mock_db, created_meetings):
        """Test that ObjectId is converted to string in returned meetings."""
        meetings = get_meetings_by_user_id("test_user_1", db=mock_db)
        
        assert len(meetings) > 0
        for meeting in meetings:
            assert "_id" in meeting
            assert isinstance(meeting["_id"], str)


# Tests for get_meeting_by_id
class TestGetMeetingById:
    
    def test_get_meeting_by_id_returns_correct_meeting(self, mock_db, created_meetings, sample_meetings_data):
        """Test that get_meeting_by_id returns the correct meeting."""
        meeting_id = str(created_meetings[0])
        meeting = get_meeting_by_id(meeting_id, db=mock_db)
        
        assert meeting is not None
        assert meeting["_id"] == meeting_id
        assert meeting["title"] == "Team Standup"
        assert meeting["user_id"] == "test_user_1"
    
    def test_get_meeting_by_id_non_existent_id(self, mock_db):
        """Test getting meeting with non-existent ID."""
        from bson import ObjectId
        fake_id = str(ObjectId())
        meeting = get_meeting_by_id(fake_id, db=mock_db)
        
        assert meeting is None
    
    def test_get_meeting_by_id_invalid_id_format(self, mock_db):
        """Test getting meeting with invalid ID format."""
        meeting = get_meeting_by_id("invalid_id_format", db=mock_db)
        
        assert meeting is None
    
    def test_get_meeting_by_id_converts_object_id_to_string(self, mock_db, created_meetings):
        """Test that ObjectId is converted to string in returned meeting."""
        meeting_id = str(created_meetings[0])
        meeting = get_meeting_by_id(meeting_id, db=mock_db)
        
        assert meeting is not None
        assert "_id" in meeting
        assert isinstance(meeting["_id"], str)
        assert meeting["_id"] == meeting_id


# Tests for get_all_meetings
class TestGetAllMeetings:
    
    def test_get_all_meetings_returns_all_meetings(self, mock_db, created_meetings, sample_meetings_data):
        """Test that get_all_meetings returns all meetings in database."""
        meetings = get_all_meetings(db=mock_db)
        
        assert len(meetings) == 3
        
        # Check that all sample meetings are returned
        meeting_titles = [meeting["title"] for meeting in meetings]
        assert "Team Standup" in meeting_titles
        assert "Project Review" in meeting_titles
        assert "Client Meeting" in meeting_titles
    
    def test_get_all_meetings_empty_database(self, mock_db):
        """Test get_all_meetings when database is empty."""
        meetings = get_all_meetings(db=mock_db)
        
        assert len(meetings) == 0
        assert meetings == []
    
    def test_get_all_meetings_converts_object_ids_to_strings(self, mock_db, created_meetings):
        """Test that all ObjectIds are converted to strings."""
        meetings = get_all_meetings(db=mock_db)
        
        assert len(meetings) > 0
        for meeting in meetings:
            assert "_id" in meeting
            assert isinstance(meeting["_id"], str)


# Tests for delete_meeting_by_id
class TestDeleteMeetingById:
    
    def test_delete_meeting_by_id_successful_deletion(self, mock_db, created_meetings):
        """Test successful deletion of a meeting by ID."""
        meeting_id = str(created_meetings[0])
        
        # Verify meeting exists before deletion
        meeting_before = get_meeting_by_id(meeting_id, db=mock_db)
        assert meeting_before is not None
        
        # Delete the meeting
        result = delete_meeting_by_id(meeting_id, db=mock_db)
        assert result is True
        
        # Verify meeting no longer exists
        meeting_after = get_meeting_by_id(meeting_id, db=mock_db)
        assert meeting_after is None
    
    def test_delete_meeting_by_id_non_existent_meeting(self, mock_db):
        """Test deletion of non-existent meeting."""
        from bson import ObjectId
        fake_id = str(ObjectId())
        
        result = delete_meeting_by_id(fake_id, db=mock_db)
        assert result is False
    
    def test_delete_meeting_by_id_invalid_id_format(self, mock_db):
        """Test deletion with invalid ID format."""
        result = delete_meeting_by_id("invalid_id_format", db=mock_db)
        assert result is False
    
    def test_delete_meeting_by_id_does_not_affect_other_meetings(self, mock_db, created_meetings):
        """Test that deleting one meeting doesn't affect others."""
        meeting_id = str(created_meetings[0])
        total_meetings_before = len(get_all_meetings(db=mock_db))
        
        result = delete_meeting_by_id(meeting_id, db=mock_db)
        assert result is True
        
        total_meetings_after = len(get_all_meetings(db=mock_db))
        assert total_meetings_after == total_meetings_before - 1


# Tests for delete_meetings_by_user_id
class TestDeleteMeetingsByUserId:
    
    def test_delete_meetings_by_user_id_deletes_all_user_meetings(self, mock_db, created_meetings):
        """Test deletion of all meetings for a specific user."""
        # Verify user has meetings before deletion
        meetings_before = get_meetings_by_user_id("test_user_1", db=mock_db)
        assert len(meetings_before) == 2
        
        # Delete meetings for user
        deleted_count = delete_meetings_by_user_id("test_user_1", db=mock_db)
        assert deleted_count == 2
        
        # Verify user has no meetings after deletion
        meetings_after = get_meetings_by_user_id("test_user_1", db=mock_db)
        assert len(meetings_after) == 0
    
    def test_delete_meetings_by_user_id_single_meeting(self, mock_db, created_meetings):
        """Test deletion for user with single meeting."""
        deleted_count = delete_meetings_by_user_id("test_user_2", db=mock_db)
        assert deleted_count == 1
        
        meetings_after = get_meetings_by_user_id("test_user_2", db=mock_db)
        assert len(meetings_after) == 0
    
    def test_delete_meetings_by_user_id_no_meetings(self, mock_db, created_meetings):
        """Test deletion for user with no meetings."""
        deleted_count = delete_meetings_by_user_id("non_existent_user", db=mock_db)
        assert deleted_count == 0
    
    def test_delete_meetings_by_user_id_does_not_affect_other_users(self, mock_db, created_meetings):
        """Test that deleting one user's meetings doesn't affect other users."""
        # Count meetings for other user before deletion
        user2_meetings_before = get_meetings_by_user_id("test_user_2", db=mock_db)
        assert len(user2_meetings_before) == 1
        
        # Delete meetings for test_user_1
        deleted_count = delete_meetings_by_user_id("test_user_1", db=mock_db)
        assert deleted_count == 2
        
        # Verify test_user_2's meetings are unaffected
        user2_meetings_after = get_meetings_by_user_id("test_user_2", db=mock_db)
        assert len(user2_meetings_after) == 1
        assert user2_meetings_after[0]["title"] == "Client Meeting"


# Tests for delete_all_meetings
class TestDeleteAllMeetings:
    
    def test_delete_all_meetings_deletes_all_meetings(self, mock_db, created_meetings):
        """Test that delete_all_meetings removes all meetings."""
        # Verify meetings exist before deletion
        meetings_before = get_all_meetings(db=mock_db)
        assert len(meetings_before) == 3
        
        # Delete all meetings
        deleted_count = delete_all_meetings(db=mock_db)
        assert deleted_count == 3
        
        # Verify no meetings remain
        meetings_after = get_all_meetings(db=mock_db)
        assert len(meetings_after) == 0
    
    def test_delete_all_meetings_empty_database(self, mock_db):
        """Test delete_all_meetings on empty database."""
        deleted_count = delete_all_meetings(db=mock_db)
        assert deleted_count == 0
        
        meetings_after = get_all_meetings(db=mock_db)
        assert len(meetings_after) == 0
