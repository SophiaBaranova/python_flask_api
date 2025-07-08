import re
from datetime import datetime, timezone
from flask import abort, make_response

from config import db
from models import Event, event_schema, events_schema


# Custom exception for invalid event data
class InvalidEventData(Exception):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code


# Function to validate event data
def validate_event(event):
    error_code = 0
    error_msg = ""
    try:
        # Validate the location: City (Country)
        location_pattern = r"^[A-Za-z .'-]+ \([A-Za-z .'-]+\)$"
        if not re.match(location_pattern, event.get("location")):
            raise InvalidEventData(
                "Location must be in the format 'City (Country)'", 422)
        # Validate the date: must be in the future
        event_date = datetime.fromisoformat(event.get("date"))
        now = datetime.now(timezone.utc) if event_date.tzinfo else datetime.now()
        if event_date <= now:
            raise InvalidEventData("Event date must be in the future", 422)
        # Validate the ticket price and tickets available
        if event.get("ticket_price") < 0:
            raise InvalidEventData(
                "Ticket price must be a non-negative float number", 422)
        if event.get("tickets_available") < 0:
            raise InvalidEventData(
                "Number of tickets available must be a non-negative integer", 422)
    except InvalidEventData as e:
        error_code = e.error_code
        error_msg = str(e)
    return error_code, error_msg


# Function to set the date to ISO 8601 format without microseconds
def convert_date(event):
    formatted = event.date.strftime("%Y-%m-%dT%H:%M:%S")
    event.date = datetime.fromisoformat(formatted)
    return event


# CRUD operations for Event model


def read_all():
    events = Event.query.all()
    return events_schema.dump(events), 200


def create(event):
    name = event.get("name")
    # Check if the event already exists
    if Event.query.filter_by(name=name).one_or_none():
        abort(406, f"Event with name '{name}' already exists")
    # Validate the event data
    error_code, error_msg = validate_event(event)
    if error_code != 0:
        abort(error_code, error_msg)
    # Create a new event instance
    new_event = event_schema.load(event, session=db.session)
    # Format the date
    convert_date(new_event)
    # Add the new event to the session and commit
    db.session.add(new_event)
    db.session.commit()
    return event_schema.dump(new_event), 201


def read_one(name):
    event = Event.query.filter_by(name=name).one_or_none()
    # Check if the event exists
    if event:
        return event_schema.dump(event), 200
    else:
        abort(404, f"Event with name '{name}' not found")


def update(name, event):
    # Check if the event exists
    existing_event = Event.query.filter_by(name=name).one_or_none()
    if not existing_event:
        abort(404, f"Event with name '{name}' not found")
    # Validate the event data
    error_code, error_msg = validate_event(event)
    if error_code != 0:
        abort(error_code, error_msg)
    # Create a new event instance
    update_event = event_schema.load(event, session=db.session)
    # Format the date
    convert_date(update_event)
    # Update the existing event with new data
    existing_event.date = update_event.date
    existing_event.location = update_event.location
    existing_event.ticket_price = update_event.ticket_price
    existing_event.tickets_available = update_event.tickets_available
    # Merge the updated event into the session and commit
    db.session.merge(existing_event)
    db.session.commit()
    return event_schema.dump(existing_event), 200


def delete(name):
    # Check if the event exists
    existing_event = Event.query.filter_by(name=name).one_or_none()
    if existing_event:
        # Delete the event from the session and commit
        db.session.delete(existing_event)
        db.session.commit()
        return make_response(f"Event '{name}' successfully deleted", 204)
    else:
        abort(404, f"Event with name '{name}' not found")
