def test_get_activities_returns_activity_list(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_signup_adds_normalized_participant(client):
    response = client.post("/activities/Chess%20Club/signup?email=NewStudent@mergington.edu")

    assert response.status_code == 200
    assert response.json()["message"] == "Signed up newstudent@mergington.edu for Chess Club"

    activities = client.get("/activities").json()
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]


def test_duplicate_signup_case_insensitive(client):
    response = client.post("/activities/Chess%20Club/signup?email=Michael@mergington.edu")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_remove_participant(client):
    response = client.delete("/activities/Chess%20Club/signup?email=michael@mergington.edu")

    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"

    activities = client.get("/activities").json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_remove_nonexistent_participant_returns_error(client):
    response = client.delete("/activities/Gym%20Class/signup?email=someone@mergington.edu")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_missing_activity_returns_not_found(client):
    response = client.post("/activities/NotAClub/signup?email=test@mergington.edu")
    assert response.status_code == 404

    response = client.delete("/activities/NotAClub/signup?email=test@mergington.edu")
    assert response.status_code == 404
