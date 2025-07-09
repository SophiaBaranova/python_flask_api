def test_read_all_events(client):
    # Read all events
    response = client.get("/api/events")
    # Assert the response
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) > 0


def test_create_event_success(client):
    # Create a new event
    new_event = {
        "name": "Test Event",
        "date": "2026-01-01T12:00:00",
        "location": "Test City (Test Country)",
        "ticket_price": 20.0,
        "tickets_available": 100
    }
    # Post the event
    response = client.post("/api/events", json=new_event)
    # Assert the response
    assert response.status_code == 201
    assert response.json["name"] == new_event["name"]


def test_create_event_duplicate_name(client):
    # Create a new event
    new_event = {
        "name": "Duplicate Event",
        "date": "2026-01-01T12:00:00",
        "location": "Duplicate City (Duplicate Country)",
        "ticket_price": 20.0,
        "tickets_available": 100
    }
    # Post the event
    response = client.post("/api/events", json=new_event)
    # Assert the response
    assert response.status_code == 201
    # Try to create a duplicate event
    response = client.post("/api/events", json=new_event)
    # Assert the response
    assert response.status_code == 406
    assert f"Event with name '{new_event["name"]}' already exists" in response.json[
        "detail"]


def test_create_event_invalid_location(client):
    # Create a new event with an invalid location format
    new_event = {
        "name": "Invalid Location Event",
        "date": "2026-01-01T12:00:00",
        "location": "InvalidLocation",
        "ticket_price": 20.0,
        "tickets_available": 100
    }
    # Try to post the event
    response = client.post("/api/events", json=new_event)
    # Assert the response
    assert response.status_code == 422
    assert "Location must be in the format 'City (Country)'" in response.json[
        "detail"]


def test_create_event_past_date(client):
    # Create a new event with a past date
    new_event = {
        "name": "Past Date Event",
        "date": "2020-01-01T12:00:00",
        "location": "Past City (Past Country)",
        "ticket_price": 20.0,
        "tickets_available": 100
    }
    # Try to post the event
    response = client.post("/api/events", json=new_event)
    # Assert the response
    assert response.status_code == 422
    assert "Event date must be in the future" in response.json["detail"]


def test_create_event_negative_price(client):
    # Create a new event with a negative ticket price
    new_event = {
        "name": "Negative Price Event",
        "date": "2026-01-01T12:00:00",
        "location": "Negative Price City (Negative Price Country)",
        "ticket_price": -10.0,
        "tickets_available": 100
    }
    # Try to post the event
    response = client.post("/api/events", json=new_event)
    # Assert the response
    assert response.status_code == 422
    assert "Ticket price must be a non-negative float number" in response.json[
        "detail"]


def test_create_event_negative_tickets(client):
    # Create a new event with negative number of tickets available
    new_event = {
        "name": "Negative Tickets Event",
        "date": "2026-01-01T12:00:00",
        "location": "Negative Tickets City (Negative Tickets Country)",
        "ticket_price": 20.0,
        "tickets_available": -5
    }
    # Try to post the event
    response = client.post("/api/events", json=new_event)
    # Assert the response
    assert response.status_code == 422
    assert "Number of tickets available must be a non-negative integer" in response.json[
        "detail"]


def test_read_one_event_success(client):
    # Create a new event
    new_event = {
        "name": "Read Event",
        "date": "2026-01-01T12:00:00",
        "location": "Read City (Read Country)",
        "ticket_price": 20.0,
        "tickets_available": 100
    }
    # Post the event
    response = client.post("/api/events", json=new_event)
    # Assert the response
    assert response.status_code == 201
    # Read the event
    response = client.get(f"/api/events/{new_event["name"]}")
    # Assert the response
    assert response.status_code == 200
    assert response.json["name"] == new_event["name"]


def test_read_one_event_not_found(client):
    # Try to read a non-existent event
    event_name = "Nonexistent Event"
    response = client.get(f"/api/events/{event_name}")
    # Assert the response
    assert response.status_code == 404
    assert f"Event with name '{event_name}' not found" in response.json[
        "detail"]


def test_update_event_success(client):
    # Create a new event
    new_event = {
        "name": "Update Event",
        "date": "2026-01-01T12:00:00",
        "location": "Update City (Update Country)",
        "ticket_price": 20.0,
        "tickets_available": 100
    }
    # Post the event
    response = client.post("/api/events", json=new_event)
    # Assert the response
    assert response.status_code == 201
    # Create an updated event
    updated_event = {
        "name": "Updated Event",
        "date": "2026-02-01T12:00:00",
        "location": "Updated City (Updated Country)",
        "ticket_price": 25.0,
        "tickets_available": 150
    }
    # Update the event
    response = client.put(f"/api/events/{new_event["name"]}", json=updated_event)
    # Assert the response
    assert response.status_code == 200
    assert response.json["name"] == updated_event["name"]


def test_update_event_not_found(client):
    # Create a new event
    updated_event = {
        "name": "Nonexistent Event",
        "date": "2026-02-01T12:00:00",
        "location": "Nonexistent City (Nonexistent Country)",
        "ticket_price": 25.0,
        "tickets_available": 150
    }
    # Try to update a non-existent event
    response = client.put(f"/api/events/{updated_event["name"]}", 
                          json=updated_event)
    # Assert the response
    assert response.status_code == 404
    assert f"Event with name '{updated_event["name"]}' not found" in response.json[
        "detail"]


def test_delete_event_success(client):
    # Create a new event
    new_event = {
        "name": "Delete Event",
        "date": "2026-01-01T12:00:00",
        "location": "Delete City (Delete Country)",
        "ticket_price": 20.0,
        "tickets_available": 100
    }
    # Post the event
    response = client.post("/api/events", json=new_event)
    # Assert the response
    assert response.status_code == 201
    # Delete the created event
    response = client.delete(f"/api/events/{new_event["name"]}")
    # Assert the response
    assert response.status_code == 204
    # Try to read the event
    response = client.get(f"/api/events/{new_event["name"]}")
    # Assert the response
    assert response.status_code == 404
    assert f"Event with name '{new_event["name"]}' not found" in response.json[
        "detail"]


def test_delete_event_not_found(client):
    # Try to delete a non-existent event
    event_name = "Nonexistent Event"
    response = client.delete(f"/api/events/{event_name}")
    # Assert the response
    assert response.status_code == 404
    assert f"Event with name '{event_name}' not found" in response.json[
        "detail"]
