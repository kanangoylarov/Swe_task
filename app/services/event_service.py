import requests
import os
from app.models.event import Event, db
from werkzeug.utils import secure_filename
from datetime import date
import datetime
EVENTS = [
    {
        "id": 1,
        "title": "Tech Innovators Conference",
        "author": "John Doe",
        "start": "2024-10-12T09:00:00",
        "end": "2024-10-12T17:00:00",
        "location": "Silicon Valley Conference Center"
    },
    {
        "id": 2,
        "title": "AI & Machine Learning Expo",
        "author": "Jane Smith",
        "start": "2024-11-05T10:00:00",
        "end": "2024-11-05T18:00:00",
        "location": "New York Convention Hall"
    },
    {
        "id": 3,
        "title": "Web Development Workshop",
        "author": "Michael Johnson",
        "start": "2024-09-20T08:00:00",
        "end": "2024-09-20T12:00:00",
        "location": "Los Angeles Tech Hub"
    },
    {
        "id": 4,
        "title": "Cloud Computing Summit",
        "author": "Emily Davis",
        "start": "2024-12-15T09:00:00",
        "end": "2024-12-15T16:00:00",
        "location": "Chicago IT Arena"
    },
    {
        "id": 5,
        "title": "Cybersecurity Awareness Day",
        "author": "Robert Williams",
        "start": "2024-10-22T11:00:00",
        "end": "2024-10-22T15:00:00",
        "location": "Boston Security Hub"
    },
    {
        "id": 6,
        "title": "Startups & Entrepreneurs Meetup",
        "author": "Linda Martinez",
        "start": "2024-09-28T14:00:00",
        "end": "2024-09-28T18:00:00",
        "location": "San Francisco Startup Center"
    },
    {
        "id": 7,
        "title": "Big Data Analytics Conference",
        "author": "David Anderson",
        "start": "2024-11-17T09:00:00",
        "end": "2024-11-17T17:00:00",
        "location": "Seattle Data Hub"
    },
    {
        "id": 8,
        "title": "Fintech Innovations Forum",
        "author": "Sophia Brown",
        "start": "2024-12-05T10:00:00",
        "end": "2024-12-05T16:00:00",
        "location": "Dallas Fintech Center"
    },
    {
        "id": 9,
        "title": "UX/UI Design Bootcamp",
        "author": "Chris Wilson",
        "start": "2024-10-18T09:00:00",
        "end": "2024-10-18T13:00:00",
        "location": "Denver Design Studio"
    },
    {
        "id": 10,
        "title": "Blockchain Technology Expo",
        "author": "Ashley Taylor",
        "start": "2024-11-25T09:00:00",
        "end": "2024-11-25T15:00:00",
        "location": "Miami Blockchain Arena"
    }
]


EVENTS_API_URL = "https://api.example.com/events"

def fetch_events():
    return EVENTS
    try:
        response = requests.get(EVENTS_API_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching events: {e}")
        return None

def local_events():
    events = Event.query.all()
    return events

def fetch_admin_events():
    """Fetch events from an external API and merge them with locally stored events."""
    try:
        api_events = fetch_events() or []
        
        # Get locally stored events with images
        local_events = Event.query.all()
        local_events_dict = {event.id: event for event in local_events}
        print(local_events)
        # Merge API events with local ones (keeping local image paths)
        merged_events = []
        for api_event in api_events:
            event_id = api_event['id']
            if event_id in local_events_dict:
                # Attach local event's image path to the API event
                api_event['image_path'] = local_events_dict[event_id].image_path
            else:
                # No image attached to this API event
                api_event['image_path'] = None

            merged_events.append(api_event)

        return merged_events
    except requests.exceptions.RequestException as e:
        print(f"Error fetching events: {e}")
        return None



UPLOAD_FOLDER = 'app/static/event_images'

def remove_image_and_event(event_id):
    """Remove the attached image and delete the event from the local database."""
    # Fetch the event from the local database
    event = Event.query.get(event_id)

    if event:
        # Check if the event has an attached image
        if event.image_path:
            # Remove the image file from the file system
            try:
                os.remove(os.path.join(UPLOAD_FOLDER, event.image_path))
            except OSError as e:
                raise Exception(f"Error removing image file: {e}")

        # Remove the event from the database
        db.session.delete(event)
        db.session.commit()
        return event.title
    else:
        raise Exception(f"No local event found with ID {event_id}.")
    
UPLOAD_FOLDER = 'app/static/event_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Check if the file is of an allowed type."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(file):
    """Save the uploaded image and return its filename."""
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    return filename

def parse_datetime(date_str):
    """Parse a datetime string in 'YYYY-MM-DDTHH:MM:SS' format to a datetime object."""
    return datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')

def attach_image_to_event(event_id, file):
    """Attach an image to an event and store the event locally if not already stored."""
    if not allowed_file(file.filename):
        raise Exception("File type not allowed")

    filename = save_image(file)
    
    # Check if event exists locally
    event = Event.query.get(event_id)

    if not event:
        # Fetch the event details from the external API
        events = fetch_events()
        api_event = next((e for e in events if e['id'] == event_id), None)

        if not api_event:
            raise Exception(f"Event with ID {event_id} not found in API.")
        
        start_time = parse_datetime(api_event['start'])
        end_time = parse_datetime(api_event['end'])

        # Create the local event and attach the image
        event = Event(
            id=api_event['id'],
            title=api_event['title'],
            author=api_event['author'],
            start=start_time,
            end=end_time,
            location=api_event['location'],
            image_path=filename
        )
        db.session.add(event)
    else:
        # Update existing event with the new image
        event.image_path = filename
    
    db.session.commit()
    return event.title
