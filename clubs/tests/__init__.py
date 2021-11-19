rom django import forms
from django.test import TestCase
from clubs.models import User
from clubs.forms import UserUpdateForm, SignUpForm

# Used this from clucker project with some modifications
class userUpdateViewTestCase(TestCase):
    def setUp(self):
        self.valid_form_input = {
            'email': 'bobsmith@example.org',
            'first_name': 'Bob',
            'last_name': 'Smith',
            'bio': 'Hi',
            'chess_experience': 'BG',
            'personal_statement': 'I am Orangutan',
            'new_password': 'Password123',
            'password_confirmation': 'Password123'
        }
