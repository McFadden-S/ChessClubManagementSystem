"""Unit tests for the log in form."""
from clubs.forms import LogInForm
from django import forms
from clubs.models import User
from django.test import TestCase


class LogInFormTestCase(TestCase):
    """Unit tests for the log in form."""

    fixtures = ['clubs/tests/fixtures/default_user.json']

    def setUp(self):
        self.form_input = {'email': 'bobsmith@example.org', 'password': 'Password123'}

    def test_log_in_form_contains_required_fields(self):
        """Check if the log in form contains email and password fields."""

        form = LogInForm()
        self.assertIn('email', form.fields)
        self.assertIn('password', form.fields)
        password_field = form.fields['password']
        self.assertTrue(isinstance(password_field.widget, forms.PasswordInput))

    """ Unit test for valid input """

    def test_form_accepts_valid_input(self):
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    """ Unit test for email """

    def test_form_rejects_blank_email(self):
        self.form_input['email'] = ''
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    """ Unit test for password """

    def test_form_rejects_blank_password(self):
        self.form_input['password'] = ''
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_incorrect_password_format(self):
        self.form_input['password'] = 'abc'
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    """ Unit test for authentication """

    def test_can_authenticate_valid_user(self):
        fixture = User.objects.get(email="bobsmith@example.org")
        form = LogInForm(data=self.form_input)
        user = form.get_user()
        self.assertEqual(user, fixture)

    def test_invalid_credentials_do_not_authenticate(self):
        form_input = {'email': 'bobsmith@example.org', 'password': 'WrongPassword123'}
        form = LogInForm(data=form_input)
        user = form.get_user()
        self.assertEqual(user, None)

    def test_blank_password_does_not_authenticate(self):
        form_input = {'email': 'bobsmith@example.org', 'password': ''}
        form = LogInForm(data=form_input)
        user = form.get_user()
        self.assertEqual(user, None)

    def test_blank_email_does_not_authenticate(self):
        form_input = {'email': '', 'password': 'Password123'}
        form = LogInForm(data=form_input)
        user = form.get_user()
        self.assertEqual(user, None)
