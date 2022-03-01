from django import forms
from django.utils.datastructures import MultiValueDict

from .models import UserData
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.

class NewUserForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=True, widget=forms.EmailInput)
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)

    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name",)

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)

        if commit:
            user.save()
            ud = UserData(user=user)
            ud.save()
        return user


class EditUser(forms.ModelForm):
    email = forms.EmailField(label="Email", required=True, widget=forms.EmailInput)
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)

    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name",)

    # This is some weird code that lets you magically set the initial values of the form
    # I found it here >>> https://www.peterbe.com/plog/initial-values-bound-django-form-rendered
    # I think it works by taking all the initial inputs and repackages them into a un-bounded form
    # that then lets you populate the initial values
    def __init__(self, data, **kwargs):
        initial = kwargs.get("initial", {})
        data = MultiValueDict({**{k: [v] for k, v in initial.items()}, **data})
        super().__init__(data, **kwargs)


class MoneyForm(forms.ModelForm):
    money = forms.DecimalField(label="Amount", required=True, decimal_places=2)

    class Meta:
        model = UserData
        fields = ("money",)
