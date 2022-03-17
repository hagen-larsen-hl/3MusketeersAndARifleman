from django import forms
from django.utils.datastructures import MultiValueDict

from .models import UserData
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from localflavor import us
from .models import UserData

class SplitPhoneNumberField(forms.MultiValueField):
    def __init__(self, **kwargs):
        widget = forms.MultiWidget(
            widgets={
                "area_code": forms.NumberInput,
                "prefix": forms.NumberInput,
                "line_number": forms.NumberInput,
            }
        )
        widget.decompress = lambda data: data.replace("-", " ").replace(r'[\(\)]', '').split(" ") if data else [None, None, None]
        error_messages = {"incomplete": "Enter a valid phone number.",}
        validator = lambda digits: RegexValidator(r'^[0-9]{' + str(digits) + r'}$', "Enter a valid phone number.")
        fields = (
            forms.CharField(
                error_messages=error_messages,
                validators=[validator(3)],
            ),
            forms.CharField(
                error_messages=error_messages,
                validators=[validator(3)],
            ),
            forms.CharField(
                error_messages=error_messages,
                validators=[validator(4)],
            ),
        )
        super(SplitPhoneNumberField, self).__init__(error_messages=error_messages, fields=fields, widget=widget, **kwargs)

    def compress(self, data):
        if data:
            return f"({data[0]}) {data[1]}-{data[2]}"
        return None

class NewUserForm(UserCreationForm):

    email = forms.EmailField(label=("Email"), required=True, widget=forms.EmailInput, help_text="A valid email address")
    first_name = forms.CharField(label="First Name", required=True) 

    last_name = forms.CharField(label="Last Name", required=True)
    phone_number = SplitPhoneNumberField(label="Phone Number", require_all_fields=True)
    #phone_number = forms.CharField(label="Phone Number", required=True, validators=[RegexValidator(r'^\d{8,16}$', "Enter a valid phone number with no special characters or spaces")], max_length=16)
    account_type = forms.ChoiceField(label="Account Type", choices=[("customer", "Customer"), ("worker", "Worker")], required=True, widget=forms.RadioSelect(attrs={"data": "account_type_radio"}))

    # Customer Fields (prepend with "c_")
    c_street = forms.CharField(label="Address*", max_length=128, required=False, widget=forms.TextInput(attrs={"placeholder": "Street Address*"}))
    c_street2 = forms.CharField(label="", max_length=16, required=False, widget=forms.TextInput(attrs={"placeholder": "Address 2", "no-require": True}))
    c_city = forms.CharField(label="", max_length=32, required=False, widget=forms.TextInput(attrs={"style": "width:50%;float:left", "placeholder": "City*"}))
    c_state = us.forms.USStateField(label="", required=False, widget=forms.Select(choices=[('XX', "State*"), *us.us_states.US_STATES], attrs={"style": "width:50%;float:right"}))
    c_zip_code = us.forms.USZipCodeField(label="", required=False, widget=forms.TextInput(attrs={"placeholder": "Zip Code*"}))

    # Worker Fields (prepend with "w_")

    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name",)
 
    def clean(self):
        cleaned_data = super(NewUserForm, self).clean()
        required_empties = []
        account_type = cleaned_data["account_type"]
        for k, v in cleaned_data.items():
            if k.startswith(account_type[:1] + "_") and v == "":
                required_empties.append(k)
        for empty in required_empties:
            self.add_error(empty, ValidationError("This field is required."))
        if account_type not in ["customer", "worker"]:
            self.add_error("account_type", ValidationError("An account type must be selected"))
        return cleaned_data

    def standard_fields(self):
        fields = []
        for k, v in self.fields.items():
            if not (k.startswith("c_") or k.startswith("w_")):
                fields.append(v.get_bound_field(self, k))
        return fields
    
    def customer_fields(self):
        fields = []
        for k, v in self.fields.items():
            if k.startswith("c_"):
                fields.append(v.get_bound_field(self, k))
        return fields
    
    def worker_fields(self):
        fields = []
        for k, v in self.fields.items():
            if k.startswith("w_"):
                fields.append(v.get_bound_field(self, k))
        return fields

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        self.user_data = {
            "user": user,
            "phone_number": self.cleaned_data.get("phone_number"),
        }

        if self.cleaned_data.get("account_type") == "customer":
            self.customer_data = {
                "user": user,
                # **self.cleaned_data.get("address"), TODO: Fix
            }
        #elif self.cleaned_data.get("account_type") == "worker":
        #    self.worker_data = {
        #        "user": user,
        #    }

        if commit:
            user.save()
            UserData.objects.create(**self.user_data)
            if hasattr(self, "customer_data"):
                CustomerData.objects.create(**self.customer_data)
        #    if hasattr(self, "worker_data"):
        #        WorkerData.objects.create(**self.worker_data)
        return user


class EditUser(forms.ModelForm):
    email = forms.EmailField(label="Email", required=True, widget=forms.EmailInput)
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)

    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name",)


class MoneyForm(forms.ModelForm):
    money = forms.DecimalField(label="Amount", required=True, decimal_places=2)

    class Meta:
        model = UserData
        fields = ("money",)
