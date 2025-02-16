from django.urls import path
from .views import timetable_view, get_events, add_session, confirmation_modal, edit_modal

urlpatterns = [
    path('', timetable_view, name='timetable'),
    path('get-events/', get_events, name='get_events'),
    path('add-session/', add_session, name='add_session'),
    path('modal/confirm/<int:event_id>/', confirmation_modal, name='confirmation_modal'),
    path('modal/edit/<int:event_id>/', edit_modal, name='edit_modal'),

]
