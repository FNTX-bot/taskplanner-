from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    REPEAT_CHOICES = [
        ('none', 'None'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    due_datetime = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    repeat = models.CharField(max_length=10, choices=REPEAT_CHOICES, default='none')
    reminder_offset = models.PositiveIntegerField(
        default=30,
        help_text='Minutes before due time to show an in-app reminder',
    )
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['due_datetime']

    def __str__(self):
        return self.title

    def is_overdue(self):
        return not self.is_done and timezone.now() > self.due_datetime

    def needs_reminder(self):
        """True once we are within reminder_offset minutes of due time (or past it)."""
        reminder_time = self.due_datetime - timedelta(minutes=self.reminder_offset)
        return not self.is_done and timezone.now() >= reminder_time
