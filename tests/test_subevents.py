def test_create_subevent_success(client):
    # Create a new subevent
    new_subevent = {
        "name": "Create Subevent",
        "time": "10:00:00",
        "event_id": 1
    }
    # Post the subevent
    response = client.post("/api/subevents", json=new_subevent)
    # Assert the response
    assert response.status_code == 201
    assert response.json["name"] == new_subevent["name"]


def test_create_subevent_invalid_event_id(client):
    # Create a new subevent with a non-existent event_id
    new_subevent = {
        "name": "Invalid Event ID Subevent",
        "time": "10:00:00",
        "event_id": 9999
    }
    # Try to post the subevent
    response = client.post("/api/subevents", json=new_subevent)
    # Assert the response
    assert response.status_code == 404
    assert f"Event not found for ID: {new_subevent["event_id"]}" in response.json[
        "detail"]


def test_read_one_subevent_success(client):
    # Create a new subevent
    new_subevent = {
        "name": "Read Subevent",
        "time": "10:00:00",
        "event_id": 1
    }
    # Post the subevent
    response = client.post("/api/subevents", json=new_subevent)
    # Assert the response
    assert response.status_code == 201
    subevent_id = response.json["id"]
    # Read the created subevent
    response = client.get(f"/api/subevents/{subevent_id}")
    # Assert the response
    assert response.status_code == 200
    assert response.json["name"] == new_subevent["name"]


def test_read_one_subevent_not_found(client):
    # Attempt to read a non-existent subevent
    subevent_id = 9999
    response = client.get(f"/api/subevents/{subevent_id}")
    # Assert the response
    assert response.status_code == 404
    assert f"Subevent with ID '{subevent_id}' not found" in response.json[
        "detail"]


def test_update_subevent_success(client):
    # Create a new subevent
    new_subevent = {
        "name": "Update Subevent",
        "time": "10:00:00",
        "event_id": 1
    }
    # Post the subevent
    response = client.post("/api/subevents", json=new_subevent)
    # Assert the response
    assert response.status_code == 201
    subevent_id = response.json["id"]
    # Create an updated subevent
    updated_subevent = {
        "name": "Updated Subevent",
        "time": "11:00:00"
    }
    # Update the subevent
    response = client.put(f"/api/subevents/{subevent_id}", json=updated_subevent)
    # Assert the response
    assert response.status_code == 200
    assert response.json["name"] == updated_subevent["name"]


def test_update_subevent_not_found(client):
    # Create a new subevent
    updated_subevent = {
        "name": "Non-existent Subevent",
        "time": "11:00:00"
    }
    # Try to update a non-existent subevent
    subevent_id = 9999
    response = client.put(f"/api/subevents/{subevent_id}", json=updated_subevent)
    # Assert the response
    assert response.status_code == 404
    assert f"Subevent with ID '{subevent_id}' not found" in response.json[
        "detail"]


def test_delete_subevent_success(client):
    # Create a new subevent
    new_subevent = {
        "name": "Delete Subevent",
        "time": "10:00:00",
        "event_id": 1
    }
    # Post the subevent
    response = client.post("/api/subevents", json=new_subevent)
    # Assert the response
    assert response.status_code == 201
    subevent_id = response.json["id"]
    # Delete the subevent
    response = client.delete(f"/api/subevents/{subevent_id}")
    # Assert the response
    assert response.status_code == 204


def test_delete_subevent_not_found(client):
    # Try to delete a non-existent subevent
    subevent_id = 9999
    response = client.delete(f"/api/subevents/{subevent_id}")
    # Assert the response
    assert response.status_code == 404
    assert f"Subevent with ID '{subevent_id}' not found" in response.json[
        "detail"]

