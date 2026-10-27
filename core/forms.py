from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Ticket, Feedback


class RegisterForm(UserCreationForm):
    username = forms.CharField(label="Логин", min_length=6)
    email = forms.EmailField(label="Email", required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "full_name", "phone", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean_username(self):
        username = self.cleaned_data["username"]
        if not username.isascii() or not username.isalnum():
            raise forms.ValidationError("Только латиница и цифры")
        return username

    def clean_full_name(self):
        name = self.cleaned_data["full_name"]
        if not name.strip() or not all("А" <= c <= "я" or c in "Ёё " for c in name):
            raise forms.ValidationError("Только кириллица и пробелы")
        return name


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["topic", "description", "desired_date", "request_date", "priority"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "desired_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "request_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = (
                "form-select"
                if isinstance(field.widget, forms.Select)
                else "form-control"
            )


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["text"]
        widgets = {"text": forms.Textarea(attrs={"class": "form-control", "rows": 3})}
