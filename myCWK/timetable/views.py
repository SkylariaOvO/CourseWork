from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from .models import StudySession

@login_required
def timetable_view(request):
    """Renders the timetable view."""
    return render(request, 'timetable/timetable.html')

@login_required
def get_events(request):
    events = StudySession.objects.filter(student=request.user).values(
        "id", "subject", "teacher", "date", "start_time", "end_time", "location", 
        "event_type", "requires_confirmation", "attendance_status"
    )

    data = [
        {
            "id": event["id"],
            "title": event["subject"],
            "start": f"{event['date']}T{event['start_time']}",
            "end": f"{event['date']}T{event['end_time']}",
            "extendedProps": {
                "teacher": event["teacher"],
                "location": event["location"],
                "type": event["event_type"] if event["event_type"] else "student", 
                "requires_confirmation": event["requires_confirmation"],
                "attendance_status": event["attendance_status"]
            }
        }
        for event in events
    ]

    return JsonResponse(data, safe=False)



@login_required
def add_session(request):
    if request.method == "POST":
        subject = request.POST.get("subject", "").strip()
        teacher = request.POST.get("teacher", "").strip()
        date = request.POST.get("date", "").strip()
        start_time = request.POST.get("start_time", "").strip()
        end_time = request.POST.get("end_time", "").strip()
        location = request.POST.get("location", "").strip()

        # Validate input fields
        if not all([subject, teacher, date, start_time, end_time, location]):
            return JsonResponse({'success': False, 'error': "Please fill out all the fields!"})

        # Determine the event type
        event_type = "student"  # Default to student event
        if request.user.is_staff:  # If user is an admin
            event_type = "admin"

        # Prevent duplicate sessions
        existing_session = StudySession.objects.filter(
            student=request.user,
            subject=subject,
            date=date,
            start_time=start_time
        ).exists()

        if existing_session:
            return JsonResponse({'success': False, 'error': "You already have a session scheduled at this time!"})

        try:
            StudySession.objects.create(
                student=request.user,
                subject=subject,
                teacher=teacher,
                date=date,
                start_time=start_time,
                end_time=end_time,
                location=location,
                event_type=event_type, 
                attendance_status="Pending"
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return render(request, 'timetable/add_session.html')


def confirmation_modal(request, event_id):
    event = get_object_or_404(StudySession, id=event_id)
    return render(request, 'timetable/confirmation_modal.html', {'event': event})

def edit_modal(request, event_id):
    event = get_object_or_404(StudySession, id=event_id)
    return render(request, 'timetable/edit_modal.html', {'event': event})
