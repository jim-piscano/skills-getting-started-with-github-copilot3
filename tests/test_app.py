def test_root_redirects_to_frontend(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_for_activity(client):
    response = client.post(
        "/activities/Art%20Club/signup",
        params={"email": "student+art@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == (
        "Signed up student+art@mergington.edu for Art Club"
    )
    assert "student+art@mergington.edu" in client.get("/activities").json()["Art Club"]["participants"]


def test_signup_unknown_activity(client):
    response = client.post(
        "/activities/Unknown%20Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_participant(client):
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_from_activity(client):
    response = client.delete(
        "/activities/Chess%20Club/signup",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == (
        "Unregistered michael@mergington.edu from Chess Club"
    )
    assert "michael@mergington.edu" not in client.get("/activities").json()["Chess Club"]["participants"]


def test_unregister_unknown_activity(client):
    response = client.delete(
        "/activities/Unknown%20Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_unknown_participant(client):
    response = client.delete(
        "/activities/Chess%20Club/signup",
        params={"email": "unknown@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"
