from django import forms
from .models import Job


class NewJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ("time_estimate", "zip_code", "bid", "completion_window_start", "completion_window_end", "type")
