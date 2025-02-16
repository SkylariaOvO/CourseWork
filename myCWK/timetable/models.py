from django.db import models
from django.contrib.auth.models import User

class StudySession(models.Model):
    EVENT_TYPES = [
        ('admin', 'Admin Assigned'),
        ('student', 'Student Created')
    ]

    ATTENDANCE_STATUSES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Absent', 'Absent')
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sessions")
    subject = models.CharField(max_length=100)
    teacher = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=100)
    attendance_status = models.CharField(max_length=10, choices=ATTENDANCE_STATUSES, default='Pending')
    event_type = models.CharField(max_length=10, choices=EVENT_TYPES, default='student')  # Default is student event
    requires_confirmation = models.BooleanField(default=False)  # Admin events require confirmation

    def __str__(self):
        return f"{self.subject} - {self.student.username} ({self.date} {self.start_time})"