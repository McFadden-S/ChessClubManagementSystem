from django.test import TestCase
from clubs.models import User
from clubs.forms import SignUpForm

class SignUpFormTestCase(TestCase):
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

    def test_a_valid_signup_form(self):
        form = SignUpForm(data=self.valid_form_input)
        self.assertTrue(form.is_valid())

    def test_SignUp_form_uses_model_validation(self):
        self.valid_form_input['email'] = '@example.org'
        form = SignUpForm(data=self.valid_form_input)
        self.assertFalse(form.is_valid())
