from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    required_css_class = 'required'
    first_name = forms.CharField(max_length=30, required=False,
                                 help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False,
                                help_text='Optional.')
    email = forms.EmailField(max_length=254,
                             help_text='Required. \
                                 Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1',
                  'password2', )


class EditProfileForm(UserChangeForm):
    required_css_class = 'required'
    password = None
    username = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(
                                attrs={'class': 'form-control',
                                       'readonly': 'readonly'})
                              )
    last_login = forms.DateTimeField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly'})
                                )
    first_name = forms.CharField(
        required=True, widget=forms.TextInput(
                                attrs={'class': 'form-control'})
                                )
    last_name = forms.CharField(
        required=True, widget=forms.TextInput(
                                attrs={'class': 'form-control'})
                                )
    email = forms.CharField(
        required=True, widget=forms.TextInput(
                                attrs={'class': 'form-control'})
                                )
    date_joined = forms.DateTimeField(
        required=True, widget=forms.TextInput(
                                attrs={'class': 'form-control',
                                       'readonly': 'readonly'})
                                )

    class Meta:
        model = User
        fields = ("username", "last_login", "first_name", "last_name", "email",
                  "date_joined", )
