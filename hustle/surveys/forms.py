from django.forms import ModelForm
from .models import Survey


class SurveyForm(ModelForm):
    class Meta:
        model = Survey
        fields = ['duration_rating', 'duration_notes', 'complexity_rating', 'complexity_notes', 'notes']
