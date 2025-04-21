from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from accounts.models import User


class UserCreationForm(forms.ModelForm):
    """
    A custom form for creating new users.

    Includes fields for password confirmation and handles password hashing.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'full_name', 'phone_number')

    def clean_password2(self):
        """
        Ensure the two entered passwords match.
        """
        cd = self.cleaned_data
        if cd.get('password1') and cd.get('password2') and cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords must match.')
        return cd['password2']

    def save(self, commit=True):
        """
        Save the user instance with a hashed password.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    A form for updating users in the admin panel.

    Displays password as a read-only hash field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'full_name', 'phone_number')

    def clean_password(self):
        """
        Return the initial password value (unchanged).
        """
        return self.initial['password']


class UserLoginForm(forms.Form):
    """
    A basic login form with email and password fields.
    """
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegistrationForm(forms.Form):
    """
    A registration form for new users.

    Includes fields for email, full name, phone number, and password.
    """
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(
        max_length=12,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
