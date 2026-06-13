from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'due_datetime', 'priority', 'repeat', 'reminder_offset']
        widgets = {
            'due_datetime': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
            'title': forms.TextInput(attrs={'placeholder': 'Task title…'}),
            'reminder_offset': forms.NumberInput(attrs={'min': '0', 'placeholder': '30'}),
        }
        labels = {
            'due_datetime': 'Due Date & Time',
            'reminder_offset': 'Reminder (minutes before due)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-fill the datetime-local input for the edit form
        if self.instance and self.instance.pk and self.instance.due_datetime:
            self.initial['due_datetime'] = self.instance.due_datetime.strftime('%Y-%m-%dT%H:%M')
