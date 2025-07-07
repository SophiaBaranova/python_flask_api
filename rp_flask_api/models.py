from datetime import datetime
from config import db, ma

class Event(db.Model):
    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    date = db.Column(db.DateTime)
    location = db.Column(db.String(32))
    ticket_price = db.Column(db.Float)
    tickets_available = db.Column(db.Integer)


class EventSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Event
        load_instance = True
        sqla_session = db.session

event_schema = EventSchema()
events_schema = EventSchema(many=True)
