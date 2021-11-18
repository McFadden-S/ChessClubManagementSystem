from django import forms
from django.test import TestCase
from clubs.models import User
from clubs.forms import UserUpdateForm, SignUpForm

# Used this from clucker project with some modifications
class userUpdateFormTestCase(TestCase):
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

        self.valid_update_form_input = {
            'email': 'bobysmithy@example.org',
            'first_name': 'Bobby',
            'last_name': 'Smithy',
            'bio': 'Hello',
            'chess_experience': 'AV',
            'personal_statement': 'I am not Orangutan',
        }

    def test_form_has_necessary_fields(self):
        form = UserUpdateForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('email', form.fields)
        self.assertTrue(isinstance(form.fields['email'], forms.EmailField))
        self.assertIn('bio', form.fields)
        self.assertIn('chess_experience', form.fields)
        self.assertIn('personal_statement', form.fields)

    def test_form_is_valid(self):
        form = UserUpdateForm(data=self.valid_update_form_input)
        self.assertTrue(form.is_valid())

    def test_form_uses_model_validation(self):
        self.valid_update_form_input['first_name'] = ''
        form = UserUpdateForm(data=self.valid_update_form_input)
        self.assertFalse(form.is_valid())

    def test_form_saves_correctly(self):
        sign_up_form = SignUpForm(data=self.valid_form_input)
        sign_up_form.save()
        user = User.objects.get(email='bobsmith@example.org')

        form = UserUpdateForm(instance=user, data=self.valid_update_form_input)
        before_count = User.objects.count()
        form.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)

        self.assertEqual(user.first_name, 'Bobby')
        self.assertEqual(user.last_name, 'Smithy')
        self.assertEqual(user.email, 'bobysmithy@example.org')
        self.assertEqual(user.bio, 'Hello')
        self.assertEqual(user.chess_experience, 'AV')
        self.assertEqual(user.personal_statement, 'I am not Orangutan')
