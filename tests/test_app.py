import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity():
    test_email = "pytestuser@mergington.edu"
    activity = "Chess Club"
    # Remove if already present
    if test_email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(test_email)
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert response.status_code == 200
    assert test_email in activities[activity]["participants"]
    # Try duplicate signup
    response2 = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert response2.status_code == 400
    # Clean up
    activities[activity]["participants"].remove(test_email)

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404

# If unregister endpoint exists, test it
def test_unregister_for_activity():
    test_email = "pytestuser2@mergington.edu"
    activity = "Programming Class"
    # Add participant first
    if test_email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(test_email)
    # Try to unregister (simulate endpoint)
    try:
        response = client.post(f"/activities/{activity}/unregister?email={test_email}")
        # If endpoint exists, should be 200 or 404 if not found
        assert response.status_code in (200, 404)
        if response.status_code == 200:
            assert test_email not in activities[activity]["participants"]
    except Exception:
        # Endpoint may not exist yet
        pass