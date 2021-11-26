from django import forms
from .models import User, Club_Member, Club
from django.core.validators import RegexValidator
import requests
import urllib.parse
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
    def clean(self):
        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')

        if new_password != password_confirmation:
            self.add_error('password_confirmation','confirmation no match password')

    def save(self):
        super().save(commit=False)

        user = User.objects.create_user(
            email=self.cleaned_data.get('email'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            bio=self.cleaned_data.get('bio'),
            personal_statement=self.cleaned_data.get('personal_statement'),
            chess_experience=self.cleaned_data.get('chess_experience'),
            password=self.cleaned_data.get('new_password'),
        )

        # Club_Member.objects.create(user=user)

        return user

# Used this from clucker project with some modifications
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','bio','chess_experience','personal_statement']
        widgets = { 'bio': forms.Textarea(), 'personal_statement': forms.Textarea()}

# Used this from clucker project with some modifications
class UserChangePasswordForm(forms.Form):
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9].*$)',
            message='password contain upper, lower and number'
        )]
    )
    new_password_confirmation = forms.CharField(label='Confirm New Password',widget=forms.PasswordInput())

    def clean(self):
        super().clean()

        new_password = self.cleaned_data.get('new_password')
        new_password_confirmation = self.cleaned_data.get('new_password_confirmation')

        if new_password != new_password_confirmation:
            self.add_error('new_password_confirmation', 'Confirmation does not match password.')

class LogInForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

class CreateClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name','address','city','postal_code','country','description']
        # validators=
        # widgets = { 'bio': forms.Textarea(), 'personal_statement': forms.Textarea()}
    def save(self):
        super().save(commit=False)
        # https://stackoverflow.com/questions/25888396/how-to-get-latitude-longitude-with-python
        full_address = f"{self.cleaned_data.get('address')}, {self.cleaned_data.get('city')}, {self.cleaned_data.get('postal_code')}, {self.cleaned_data.get('country')}"
        url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(full_address) +'?format=json'

        response = requests.get(url).json()
        lat = response[0]['lat']
        lon = response[0]['lon']
        club = Club.objects.create(
            name=self.cleaned_data.get('name'),
            address=self.cleaned_data.get('address'),
            city=self.cleaned_data.get('city'),
            postal_code=self.cleaned_data.get('postal_code'),
            country=self.cleaned_data.get('country'),
            location=f"{lat},{lon}",
            description=self.cleaned_data.get('description'),
        )

        # Club_Member.objects.create(user=user)

        return club
