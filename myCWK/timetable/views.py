from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import StudySession
from django.http import JsonResponse


@login_required
def timetable_view(request):
    return render(request, 'timetable/timetable.html')

@login_required
def get_events(request):
    events = StudySession.objects.filter(student=request.user)
    events_list = [
        {
            "title": event.subject,
            "start": f"{event.date}T{event.start_time}",
            "end": f"{event.date}T{event.end_time}",
            "teacher": event.teacher,
            "location": event.location,
        }
        for event in events
    ]
    return JsonResponse(events_list, safe=False)

@login_required
def add_session(request):
    if request.method == "POST":
        subject = request.POST.get("subject")
        teacher = request.POST.get("teacher")
        date = request.POST.get("date")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        location = request.POST.get("location")

        StudySession.objects.create(
            student=request.user,
            subject=subject,
            teacher=teacher,
            date=date,
            start_time=start_time,
            end_time=end_time,
            location=location,
            attendance_status="Pending"
        )

        return JsonResponse({'success': True})

    return render(request, 'timetable/add_session.html')