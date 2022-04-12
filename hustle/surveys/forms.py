from django.forms import ModelForm
from .models import Survey


class SurveyForm(ModelForm):
    class Meta:
        model = Survey
        fields = ['duration_notes', 'complexity_notes', 'notes']
