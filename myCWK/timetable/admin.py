from django.contrib import admin
from .models import StudySession

@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ("subject", "teacher", "date", "start_time", "end_time", "location", "event_type", "attendance_status", "get_student")
    list_filter = ("event_type", "attendance_status", "date")
    search_fields = ("subject", "teacher", "location", "student__username")

    def get_student(self, obj):
        return obj.student.username
    get_student.admin_order_field = "student"
    get_student.short_description = "Created By"
