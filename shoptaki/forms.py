from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=200, widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()

        # confirms that the two pw match
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid Username or Password")

        return cleaned_data

class FinderForm(forms.Form):
    cap_rate = forms.CharField(
                max_length=20,
                label="Cap Rate")
    loan_to_value = forms.CharField(
            max_length=20,
            label="Loan To Value")
    current_savings = forms.IntegerField(
                label="Current Savings")
    interest_rate = forms.CharField(
                    max_length=20,
                    label="Interest Rate")
    amort_sched = forms.CharField(
                        max_length=20,
                        label="Amortization Schedule")




    def clean(self):
        cleaned_data = super().clean()


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(
        max_length=200,
        label="Password",
        widget=forms.PasswordInput())
    confirm_password = forms.CharField(
        max_length=200,
        label="Confirm Password",
        widget=forms.PasswordInput())
    email = forms.CharField(
        max_length=50,
        widget=forms.EmailInput())
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)

    def clean(self):
        cleaned_data = super().clean()
        # check pw
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password did not match.")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        return username


