# api/models.py

from django.db import models
from django.contrib.auth.models import User


class DetectionEvent(models.Model):
    STATUS_CHOICES = [
        ('detected', 'Detected'),
        ('cleared', 'Cleared'),
    ]

    LIGHT_CHOICES = [
        ('OFF', 'Off'),
        ('ORANGE', 'Warning'),
    ]

    operator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    warning_light = models.CharField(max_length=10, choices=LIGHT_CHOICES, default='OFF')
    detection_duration = models.IntegerField(default=0)
    camera_zone = models.CharField(max_length=100, default='Crosswalk-01')
    confidence_score = models.FloatField(default=85.0)

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']


class SystemLog(models.Model):
    LEVEL_CHOICES = [
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
    ]

    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    message = models.TextField()
    camera_zone = models.CharField(max_length=100, default='Crosswalk-01')

    operator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']


class SystemConfig(models.Model):
    SENSITIVITY_CHOICES = [
        ('low', 'Low'),
        ('standard', 'Standard'),
        ('high', 'High'),
    ]

    operator = models.OneToOneField(User, on_delete=models.CASCADE)

    alert_threshold = models.IntegerField(default=5)
    sensitivity_mode = models.CharField(max_length=10, choices=SENSITIVITY_CHOICES, default='standard')
    confidence_cutoff = models.IntegerField(default=85)
    camera_zone = models.CharField(max_length=100, default='Crosswalk-01')
    notifications_enabled = models.BooleanField(default=True)

    updated_at = models.DateTimeField(auto_now=True)