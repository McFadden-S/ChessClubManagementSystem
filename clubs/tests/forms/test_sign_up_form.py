"""Unit Tests for the sign up form."""
from clubs.forms import SignUpForm
from clubs.models import User
from django import forms
from django.contrib.auth.hashers import check_password
from django.test import TestCase


class SignUpFormTestCase(TestCase):
    """Unit Tests for the sign up form."""
    def setUp(self):
        self.valid_form_input = {
            'email': 'bobsmith@example.com',
            'first_name': 'Bob',
            'last_name': 'Smith',
            'bio': 'Hi',
            'chess_experience': 'AV',
            'personal_statement': 'I am Orangutan',
            'new_password': 'Orangutan123',
            'password_confirmation': 'Orangutan123'
        }

    def test_valid_form(self):
        form = SignUpForm(data=self.valid_form_input)
        self.assertTrue(form.is_valid())

    def test_form_uses_user_model_validation(self):
        self.valid_form_input['email'] = '@example.org'
        form = SignUpForm(data=self.valid_form_input)
        self.assertFalse(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = SignUpForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('email', form.fields)
        emailField = form.fields['email']
        self.assertTrue(isinstance(emailField, forms.EmailField))
        self.assertIn('bio', form.fields)
        self.assertIn('chess_experience', form.fields)
        self.assertIn('personal_statement', form.fields)
        self.assertIn('new_password', form.fields)
        newPasswordWidget = form.fields['new_password'].widget
        self.assertTrue(isinstance(newPasswordWidget, forms.PasswordInput))
        self.assertIn('password_confirmation', form.fields)
        newPasswordConfirm = form.fields['password_confirmation'].widget
        self.assertTrue(isinstance(newPasswordConfirm, forms.PasswordInput))

    def test_passwords_must_use_uppercase(self):
        self.valid_form_input['new_password'] = "password123"
        self.valid_form_input['password_confirmation'] = "password123"
        form = SignUpForm(data=self.valid_form_input)
        self.assertFalse(form.is_valid())

    def test_passwords_must_use_lowercase(self):
        self.valid_form_input['new_password'] = "PASSWORD123"
        self.valid_form_input['password_confirmation'] = "PASSWORD123"
        form = SignUpForm(data=self.valid_form_input)
        self.assertFalse(form.is_valid())

    def test_passwords_must_use_number(self):
        self.valid_form_input['new_password'] = "PasswordABC"
        self.valid_form_input['password_confirmation'] = "PasswordABC"
        form = SignUpForm(data=self.valid_form_input)
        self.assertFalse(form.is_valid())

    def test_new_password_must_match_confirm_password(self):
        self.valid_form_input['password_confirmation'] = "WrongPassword123"
        form = SignUpForm(data=self.valid_form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = SignUpForm(data=self.valid_form_input)
        before_count = User.objects.count()
        form.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count + 1)

        user = User.objects.get(email='bobsmith@example.com')
        self.assertEqual(user.first_name, 'Bob')
        self.assertEqual(user.last_name, 'Smith')
        self.assertEqual(user.email, 'bobsmith@example.com')
        self.assertEqual(user.bio, 'Hi')
        self.assertEqual(user.chess_experience, 'AV')
        self.assertEqual(user.personal_statement, 'I am Orangutan')
        is_password_correct = check_password('Orangutan123', user.password)
        self.assertTrue(is_password_correct)
