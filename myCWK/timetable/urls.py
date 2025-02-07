from django.urls import path
from .views import timetable_view, get_events, add_session

urlpatterns = [
    path('', timetable_view, name='timetable'),         # Calendar view
    path('get-events/', get_events, name='get_events'), # Fetch events for FullCalendar
    path('add-session/', add_session, name='add_session'), # Add study session
]
