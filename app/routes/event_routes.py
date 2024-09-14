from flask import Blueprint, render_template, flash
from app.services.event_service import fetch_events, local_events
from flask_login import login_required


event_routes = Blueprint('event_routes', __name__)

@event_routes.route('/', methods=['GET'])
@login_required
def events_page():
    events = fetch_events()

    le = local_events()
    if events is None:
        flash('Unable to fetch events at this time.', 'danger')
        events = []

    return render_template('user_dashboard.html', events=events, local_events=le, title='Events')
