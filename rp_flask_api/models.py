from datetime import datetime
from marshmallow_sqlalchemy import fields

from rp_flask_api.config import db, ma


class Subevent(db.Model):
    __tablename__ = "subevent"
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"))
    name = db.Column(db.String(64))
    time = db.Column(db.Time)


class SubeventSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Subevent
        load_instance = True
        sqla_session = db.session
        include_fk = True


class Event(db.Model):
    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    date = db.Column(db.DateTime)
    location = db.Column(db.String(64))
    ticket_price = db.Column(db.Float)
    tickets_available = db.Column(db.Integer)
    subevents = db.relationship(
        Subevent,
        backref="event",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="asc(Subevent.time)"
    )


class EventSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Event
        load_instance = True
        sqla_session = db.session
        include_relationships = True
    subevents = fields.Nested(SubeventSchema, many=True)


subevent_schema = SubeventSchema()
event_schema = EventSchema()
events_schema = EventSchema(many=True)
