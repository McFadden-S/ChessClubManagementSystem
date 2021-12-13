"""Unit tests for the log in form."""
from clubs.forms import LogInForm
from django import forms
from django.test import TestCase

class LogInFormTestCase(TestCase):
    """Unit tests for the log in form."""
    def setUp(self):
        self.form_input = {'email': 'orangutan@example.org', 'password': 'CorrectPassword123'}

    def test_log_in_form_contains_required_fields(self):
        form = LogInForm()
        self.assertIn('email', form.fields)
        self.assertIn('password', form.fields)
        password_field = form.fields['password']
        self.assertTrue(isinstance(password_field.widget, forms.PasswordInput))

    def test_form_accepts_valid_input(self):
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_email(self):
        self.form_input['email'] = ''
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_password(self):
        self.form_input['password'] = ''
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())
