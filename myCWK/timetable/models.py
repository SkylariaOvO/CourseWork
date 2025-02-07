
from django.db import models
from django.contrib.auth.models import User

class StudySession(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sessions")
    subject = models.CharField(max_length=100)
    teacher = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=100)
    attendance_status = models.CharField(
        max_length=10,
        choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Absent', 'Absent')],
        default='Pending'
    )

    def __str__(self):
        return f"{self.subject} - {self.student.username} ({self.date} {self.start_time})"