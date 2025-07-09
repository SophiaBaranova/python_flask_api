def test_home_page(client):
    # Test the home page
    response = client.get("/")
    # Assert the response
    assert response.status_code == 200
    # Assert the title and some content
    assert b"Let's go party!" in response.data
    assert b"explore the schedule" in response.data


def test_schedule_page_success(client):
    # Create a new event
    new_event = {
        "name": "New Event",
        "date": "2026-01-01T12:00:00",
        "location": "New City (New Country)",
        "ticket_price": 20.0,
        "tickets_available": 100,
        "subevents": [
            {
                "name": "Subevent 1", 
                "time": "10:00:00"
            }
        ]
    }
    # Post the event
    response = client.post("/api/events", json=new_event)
    # Assert the response
    assert response.status_code == 201
    # Test the schedule page for the event
    response = client.get(f"/schedule/{response.json["id"]}")
    # Assert the response
    assert response.status_code == 200
    # Assert the title and some content
    assert b"Schedule" in response.data
    assert new_event["name"].encode() in response.data
    assert new_event["subevents"][0]["name"].encode() in response.data


def test_schedule_page_not_found(client):
    # Try to access a schedule page for a non-existent event
    event_id = 9999
    response = client.get(f"/schedule/{event_id}")
    # Assert the response
    assert response.status_code == 404