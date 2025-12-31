# CLEAN POSTGRESQL SETUP - NO MONGODB
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    mobile = models.CharField(max_length=10, unique=True, blank=True, null=True)
    signup_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class ActivityLog(models.Model):
    username = models.CharField(max_length=150)
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.action} at {self.timestamp}"