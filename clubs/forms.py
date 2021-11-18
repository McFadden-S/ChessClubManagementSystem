from django import forms
from .models import User
from django.core.validators import RegexValidator

# Used this from clucker project with some modifications
class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','bio','chess_experience','personal_statement']
        widgets = { 'bio': forms.Textarea(), 'personal_statement': forms.Textarea()}

    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9].*$)',
            message='password contain upper, lower and number'
        )]
    )
    password_confirmation = forms.CharField(label='Password confirmation',widget=forms.PasswordInput())

# Used this from clucker project with some modifications
class userUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','bio','chess_experience','personal_statement']
        widgets = { 'bio': forms.Textarea(), 'personal_statement': forms.Textarea()}

# Used this from clucker project with some modifications
class userChangePasswordForm(forms.Form):
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9].*$)',
            message='password contain upper, lower and number'
        )]
    )
    password_confirmation = forms.CharField(label='Confirm New Password',widget=forms.PasswordInput())
