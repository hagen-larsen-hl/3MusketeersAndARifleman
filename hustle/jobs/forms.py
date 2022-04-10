from django import forms
from .models import Job, Bid


class NewJobForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = ("time_estimate", "zip_code", "completion_window_start", "completion_window_end", "type")


class NewJobBidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["bid", "date_time"]

