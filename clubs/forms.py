from django import forms
from .models import User
from django.core.validators import RegexValidator

# Used this from clucker project with some modifications
class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','bio','chess_experience','personal_statement']
        widgets = { 'bio': forms.Textarea(), 'personal_statement': forms.Textarea()}

    newpassword = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9].*$)',
            message='password contain upper, lower and number'
        )]
    )
    passwordConfirmation = forms.CharField(label='password confirmation',widget=forms.PasswordInput())
