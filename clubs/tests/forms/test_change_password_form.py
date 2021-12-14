"""Unit tests for the change password form."""
from clubs.models import User
from clubs.forms import UserChangePasswordForm
from django.test import TestCase

# Used this from clucker project with some modifications
class UserChangePasswordFormTestCase(TestCase):
    """Unit tests for the change password form."""

    fixtures = ['clubs/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(email='bobsmith@example.org')
        self.valid_password_form_input = {
            'password' : 'Password123',
            'new_password': 'Password12345',
            'new_password_confirmation': 'Password12345'
        }

    def test_form_has_necessary_fields(self):
        """Test if the change password form contains the necessary fields."""

        form = UserChangePasswordForm()
        self.assertIn('password', form.fields)
        self.assertIn('new_password', form.fields)
        self.assertIn('new_password_confirmation', form.fields)

    def test_valid_form(self):
        """Test if the change password form accepts a valid input."""

        form = UserChangePasswordForm(data=self.valid_password_form_input)
        self.assertTrue(form.is_valid())

    """ Unit tests for password requirements """

    def test_password_must_contain_uppercase_character(self):
        self.valid_password_form_input['new_password'] = 'password123'
        self.valid_password_form_input['password_confirmation'] = 'password123'
        form = UserChangePasswordForm(data=self.valid_password_form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_lowercase_character(self):
        self.valid_password_form_input['new_password'] = 'PASSWORD123'
        self.valid_password_form_input['new_password_confirmation'] = 'PASSWORD123'
        form = UserChangePasswordForm(data=self.valid_password_form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_number(self):
        self.valid_password_form_input['new_password'] = 'PasswordABC'
        self.valid_password_form_input['new_password_confirmation'] = 'PasswordABC'
        form = UserChangePasswordForm(data=self.valid_password_form_input)
        self.assertFalse(form.is_valid())

    def test_new_password_and_password_confirmation_are_identical(self):
        self.valid_password_form_input['new_password_confirmation'] = 'WrongPassword123'
        form = UserChangePasswordForm(data=self.valid_password_form_input)
        self.assertFalse(form.is_valid())
