import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # First signup should succeed
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Second signup should fail (already signed up)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_unregister_participant():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Remove participant
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert f"Removed {email} from {activity}" in response.json()["message"]
    # Try removing again (should fail)
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]


def test_signup_invalid_activity():
    response = client.post("/activities/Nonexistent/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_invalid_activity():
    response = client.delete("/activities/Nonexistent/unregister?email=test@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
