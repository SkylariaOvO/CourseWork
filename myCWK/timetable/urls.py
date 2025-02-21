from django.urls import path
from .views import (
    timetable_view, my_events, confirm_event, edit_event, add_session, get_events, delete_event, import_excel
)

urlpatterns = [
    path('', timetable_view, name='timetable'),
    path('my-events/', my_events, name='my_events'),
    path('confirm-event/<int:event_id>/', confirm_event, name='confirm_event'),
    path('edit-event/<int:event_id>/', edit_event, name='edit_event'),
    path('add-session/', add_session, name='add_session'),
    path('get-events/', get_events, name='get_events'),
    path('delete-event/<int:event_id>/', delete_event, name='delete_event'),
    path('import-excel/', import_excel, name='import_excel')
]
