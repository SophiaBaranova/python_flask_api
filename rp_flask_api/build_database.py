from datetime import datetime

from rp_flask_api.config import app, db
from rp_flask_api.models import Event, Subevent

EVENTS = [
  {
    "date": "2025-04-03T12:00:00",
    "location": "New York (USA)",
    "name": "Vian Borchert's exhibition opening",
    "ticket_price": 20,
    "tickets_available": 200,
    "subevents": [
        ("Opening Ceremony", "12:00:00"),
        ("Artist Talk", "14:00:00"),
        ("Live Painting Session", "16:00:00")
    ]
  },
  {
    "date": "2025-05-15T16:30:00",
    "location": "Montreux (Switzerland)",
    "name": "International Jazz Festival",
    "ticket_price": 75,
    "tickets_available": 500,
    "subevents": [
        ("Opening Concert", "16:30:00"),
        ("Musicians Performances", "17:00:00")
    ]
  },
  {
    "date": "2025-06-22T10:15:00",
    "location": "San Francisco (USA)",
    "name": "Tech Future Conference 2025",
    "ticket_price": 150,
    "tickets_available": 350,
    "subevents": [
        ("Keynote Speech", "10:15:00"),
        ("Panel Discussion", "11:30:00"),
        ("Networking Lunch", "13:00:00")
    ]
  },
  {
    "date": "2025-07-10T13:00:00",
    "location": "Venice (Italy)",
    "name": "Modern Art Biennale",
    "ticket_price": 30,
    "tickets_available": 1000,
    "subevents": [
        ("Opening Ceremony", "13:00:00"),
        ("Guided Tour", "14:30:00"),
        ("Artist Meet and Greet", "16:00:00")
    ]
  },
  {
    "date": "2025-08-06T17:09:41",
    "location": "New York (USA)",
    "name": "Imagine Dragons concert",
    "ticket_price": 100,
    "tickets_available": 1000,
    "subevents": [
    ]
  }
]

with app.app_context():
    db.drop_all()
    db.create_all()
    for event in EVENTS:
        new_event = Event(name=event.get("name"),
                            date=datetime.fromisoformat(event.get("date")),
                            location=event.get("location"),
                            ticket_price=event.get("ticket_price"),
                            tickets_available=event.get("tickets_available"))
        for name, time in event.get("subevents", []):
            new_event.subevents.append(
                Subevent(
                    name=name,
                    time=datetime.strptime(time, "%H:%M:%S").time()
                    )
                )
        db.session.add(new_event)
    db.session.commit()
