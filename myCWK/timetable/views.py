from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import StudySession
from django.utils.timezone import now
from django.contrib.auth.models import User
from django import forms
import pandas as pd
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@login_required
def add_session(request):
    """Allows a user to add a new study session."""
    if request.method == "POST":
        subject = request.POST.get("subject", "").strip()
        teacher = request.POST.get("teacher", "").strip()
        date = request.POST.get("date", "").strip()
        start_time = request.POST.get("start_time", "").strip()
        end_time = request.POST.get("end_time", "").strip()
        location = request.POST.get("location", "").strip()

        # Validate required fields
        if not all([subject, teacher, date, start_time, end_time, location]):
            messages.error(request, "Please fill out all fields.")
            return redirect('add_session')

        try:
            StudySession.objects.create(
                student=request.user,
                subject=subject,
                teacher=teacher,
                date=date,
                start_time=start_time,
                end_time=end_time,
                location=location,
                event_type="student",
                attendance_status="Pending"
            )
            messages.success(request, "Study session added successfully!")
            return redirect('timetable')

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('add_session')

    return render(request, 'timetable/add_session.html')

def timetable_view(request):
    """Renders the timetable view."""
    return render(request, 'timetable/timetable.html', {'timestamp': now().timestamp()})

@login_required
def my_events(request):
    """Displays all events for the logged-in user."""
    events = StudySession.objects.filter(student=request.user)
    return render(request, 'timetable/my_events.html', {'events': events})

@login_required
def confirm_event(request, event_id):
    """Marks an event as confirmed."""
    event = get_object_or_404(StudySession, id=event_id, student=request.user)
    event.attendance_status = "Confirmed"
    event.save()
    messages.success(request, f"Event '{event.subject}' confirmed successfully!")
    return redirect('my_events')

@login_required
def get_events(request):
    """Fetch events for FullCalendar from the DB."""
    events = StudySession.objects.filter(student=request.user)

    if not events.exists():
        return JsonResponse({"error": "No events found"}, status=404)

    data = [
        {
            "id": event.id,
            "title": event.subject,
            "start": f"{event.date}T{event.start_time}",
            "end": f"{event.date}T{event.end_time}",
            "extendedProps": {
                "teacher": event.teacher,
                "location": event.location,
                "type": event.event_type if event.event_type else "student",  
                "requires_confirmation": event.requires_confirmation,
                "attendance_status": event.attendance_status
            }
        }
        for event in events
    ]
    return JsonResponse(data, safe=False)

@login_required
def edit_event(request, event_id):
    """Allows a user to edit an event."""
    event = get_object_or_404(StudySession, id=event_id, student=request.user)

    if request.method == "POST":
        event.subject = request.POST.get("subject", event.subject)
        event.teacher = request.POST.get("teacher", event.teacher)
        event.date = request.POST.get("date", event.date)
        event.start_time = request.POST.get("start_time", event.start_time)
        event.end_time = request.POST.get("end_time", event.end_time)
        event.location = request.POST.get("location", event.location)
        event.save()
        messages.success(request, f"Event '{event.subject}' updated successfully!")
        return redirect('my_events')

    return render(request, 'timetable/edit_event.html', {'event': event})

@login_required
def delete_event(request, event_id):
    """Allows a user to delete their own events but prevents admin events from being deleted."""
    event = get_object_or_404(StudySession, id=event_id, student=request.user)

    # Prevent deletion of admin-assigned events
    if event.event_type == "admin":
        messages.error(request, "You cannot delete an admin-assigned event.")
        return redirect('my_events')

    event.delete()
    messages.success(request, f"Event '{event.subject}' deleted successfully!")
    return redirect('my_events')

class ExcelImportForm(forms.Form):
    file = forms.FileField()
    student = forms.ModelChoiceField(queryset=User.objects.all(), label="Assign Events To")

@login_required
def import_excel(request):
    """Allows an admin to import study sessions from an Excel file for a selected user."""
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to access this page.")
        return redirect("timetable")

    if request.method == "POST":
        form = ExcelImportForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            selected_user = form.cleaned_data["student"]

            try:
                df = pd.read_excel(file, engine="openpyxl")
                required_columns = {"subject", "teacher", "date", "start_time", "end_time", "location", "event_type", "attendance_status"}
                if not required_columns.issubset(df.columns):
                    messages.error(request, "Excel file must contain these columns: " + ", ".join(required_columns))
                    return redirect("import_excel")

                imported_count = 0
                for _, row in df.iterrows():
                    StudySession.objects.create(
                        student=selected_user,
                        subject=row["subject"],
                        teacher=row["teacher"],
                        date=row["date"],
                        start_time=row["start_time"],
                        end_time=row["end_time"],
                        location=row["location"],
                        event_type=row["event_type"],
                        attendance_status=row["attendance_status"]
                    )
                    imported_count += 1

                messages.success(request, f"Successfully imported {imported_count} events for {selected_user.username}!")
                return redirect("timetable")

            except Exception as e:
                messages.error(request, f"Error processing file: {e}")
                return redirect("import_excel")
    else:
        form = ExcelImportForm()

    return render(request, "timetable/import_excel.html", {"form": form})



def send_admin_event_reminders():
    target_time = now() + timedelta(hours=1)
    window_start = target_time - timedelta(minutes=5)
    window_end = target_time + timedelta(minutes=5)

    # Filter for admin events happening today that haven't been reminded yet
    admin_events = StudySession.objects.filter(
        event_type="admin",
        reminder_sent=False,
        date=now().date()
    )

    for event in admin_events:
        event_datetime = datetime.combine(event.date, event.start_time)

        # Convert to timezone-aware datetime
        event_datetime = now().replace(
            year=event_datetime.year, 
            month=event_datetime.month,
            day=event_datetime.day,
            hour=event_datetime.hour,
            minute=event_datetime.minute
        )

        if window_start <= event_datetime <= window_end:
            subject = f"Reminder: Upcoming Admin Assigned Event '{event.subject}'"
            message = (
                f"Dear {event.student.username},\n\n"
                f"This is a reminder that your admin-assigned event '{event.subject}' is scheduled to start at "
                f"{event.start_time} on {event.date} at {event.location}.\n\n"
                f"Please ensure you are prepared.\n\nBest regards,\nSchool SMT Team"
            )
            recipient_list = [event.student.email]

            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
                event.reminder_sent = True
                event.save()
                logger.info(f"Reminder sent for event {event.id}.")
            except Exception as e:
                logger.error(f"Error sending reminder for event {event.id}: {e}")
