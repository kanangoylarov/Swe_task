# app/routes/admin_event_routes.py

from flask import Blueprint, request, redirect, url_for, flash, render_template
from app.services.event_service import fetch_admin_events, remove_image_and_event, attach_image_to_event
from flask_login import login_required, current_user


admin_event_routes = Blueprint('admin_event_routes', __name__)

@admin_event_routes.route('/admin/events', methods=['GET'])
@login_required
def admin_events():
    """Display admin events page with both API and local events."""
    if current_user.role != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('event_routes.events_page'))

    # Fetch merged events (API + local with images)
    events = fetch_admin_events()
    for event in events:
        print(event['image_path'])
    return render_template('admin_events.html', events=events)

@admin_event_routes.route('/admin/events/<int:event_id>/attach_image', methods=['POST'])
@login_required
def attach_image(event_id):
    """Attach an image to an event and store the event locally if not already stored."""
    if current_user.role != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('event_routes.events_page'))

    # Check if the file is in the request
    if 'image' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('admin_event_routes.admin_events'))

    file = request.files['image']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('admin_event_routes.admin_events'))

    try:
        # Call the service to handle the logic
        event_title = attach_image_to_event(event_id, file)
        flash(f'Image attached to event "{event_title}"', 'success')
    except Exception as e:
        flash(str(e), 'danger')

    return redirect(url_for('admin_event_routes.admin_events'))


@admin_event_routes.route('/admin/events/<int:event_id>/remove_image', methods=['POST'])
@login_required
def remove_image(event_id):
    """Remove the attached image and delete the event from the local database."""
    if current_user.role != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('event_routes.events_page'))

    try:
        # Call the service function to handle the logic
        event_title = remove_image_and_event(event_id)
        flash(f'Event "{event_title}" and its image have been removed.', 'success')
    except Exception as e:
        flash(str(e), 'danger')

    return redirect(url_for('admin_event_routes.admin_events'))

