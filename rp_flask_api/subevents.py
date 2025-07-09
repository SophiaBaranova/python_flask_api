from flask import make_response, abort

from rp_flask_api.config import db
from rp_flask_api.models import Subevent, Event, subevent_schema


# CRUD operations for Subevent model


def create(subevent):
    event_id = subevent.get("event_id")
    event = Event.query.get(event_id)
    # Validate the event exists
    if event:
        # Create a new Subevent instance
        new_subevent = subevent_schema.load(subevent, session=db.session)
        # Set the event relationship
        event.subevents.append(new_subevent)
        # Commmit the changes
        db.session.commit()
        return subevent_schema.dump(new_subevent), 201
    else:
        abort(
            404,
            f"Event not found for ID: {event_id}"
        )


def read_one(subevent_id):
    subevent = Subevent.query.get(subevent_id)
    # Check if the subevent exists
    if subevent:
        return subevent_schema.dump(subevent), 200
    else:
        abort(404, f"Subevent with ID '{subevent_id}' not found")


def update(subevent_id, subevent):
    existing_subevent = Subevent.query.get(subevent_id)
    # Check if the subevent exists
    if existing_subevent:
        # Update the subevent instance
        updated_subevent = subevent_schema.load(subevent, session=db.session)
        # Update the existing subevent with new data
        existing_subevent.name = updated_subevent.name
        existing_subevent.time = updated_subevent.time
        # Merge the updated subevent into the session and commit
        db.session.merge(existing_subevent)
        db.session.commit()
        return subevent_schema.dump(updated_subevent), 200
    else:
        abort(404, f"Subevent with ID '{subevent_id}' not found")


def delete(subevent_id):
    existing_subevent = Subevent.query.get(subevent_id)
    # Check if the subevent exists
    if existing_subevent:
        # Delete the subevent from the session and commit
        db.session.delete(existing_subevent)
        db.session.commit()
        return make_response(
            f"Subevent with ID '{subevent_id}' deleted", 204
        )
    else:
        abort(404, f"Subevent with ID '{subevent_id}' not found")
