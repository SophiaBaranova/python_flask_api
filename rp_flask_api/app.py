from flask import render_template

import rp_flask_api.config as config
from rp_flask_api.models import Event
from rp_flask_api.events import read_one

app = config.connex_app
app.add_api(config.basedir / "swagger.yml")


@app.route("/")
def home():
    events = Event.query.all()
    return render_template("home.html", events=events)


@app.route("/schedule/<int:event_id>")
def schedule(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template("schedule.html", event=event)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
