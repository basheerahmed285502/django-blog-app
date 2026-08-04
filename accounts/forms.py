from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label="First Name", widget=forms.TextInput(attrs=({
        "class": "form-control", "required": True
    })))
    second_name = forms.CharField(label="Second Name", widget=forms.TextInput(attrs=({
        "class": "form-control", "required": True
    })))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs=({
        "class": "form-control", "required": True
    })))
    phone_number = forms.CharField(label="Phone Number", widget=forms.TextInput(attrs=({
        "class": "form-control", "required": True
    })))
    city = forms.CharField(label="City", widget=forms.TextInput(attrs=({
        "class": "form-control", "required": True
    })))
    address = forms.CharField(label="Address", widget=forms.Textarea(
        attrs=({"class": "form-control", "required": True, "rows": 3})))

    class Meta:
        model = User
        fields = ("username", "first_name", "second_name", "email")

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            if 'username' in self.fields:
                self.fields['password1'].label = "Username"
                self.fields['username'].widget.attrs.update(
                    {"class": "form-control"})
            if 'password1' in self.fields:
                self.fields['password1'].label = "Password"
                self.fields['password1'].help_text = ""
                self.fields['password1'].widget.attrs.update(
                    {"class": "form-control"})
            if 'password2' in self.fields:
                self.fields['password2'].label = "Confirm Password"

                self.fields['password2'].help_text = ""
                self.fields['password2'].widget.attrs.update(
                    {"class": "form-control"})

        def clean(self):
            cleaned_data = super().clean()
            email = cleaned_data.get("email")

            if User.objects.filter(email=email).exists():
                self.add_error("email", "Email already exists.")

            password1 = cleaned_data.get("password1")
            password2 = cleaned_data.get("password2")

            if password1 != password2:
                self.add_error("password2", "Passwords do not match.")

            return cleaned_data


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(
        attrs={"autofocus": True, 'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '••••••••'}))
