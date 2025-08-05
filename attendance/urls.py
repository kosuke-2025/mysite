from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('record/', views.record_attendance, name='record_attendance'),
    path('list/', views.attendance_list_view, name='attendance_list'),
]