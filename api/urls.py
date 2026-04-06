from django.urls import path
from . import views

urlpatterns = [
    # AUTH
    path('auth/register/', views.register),
    path('auth/login/', views.login),

    # DETECTIONS
    path('detections/', views.detection_events),
    path('detections/latest/', views.latest_detection),

    # LOGS
    path('logs/', views.system_logs),

    # CONFIG
    path('config/', views.system_config),
]