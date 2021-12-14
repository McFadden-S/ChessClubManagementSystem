"""Unit tests for the update user form."""
from clubs.forms import UpdateUserForm
from clubs.models import User
from django import forms
from django.test import TestCase


# Used this from clucker project with some modifications
class UpdateUserFormTestCase(TestCase):
    """Unit tests for the update user form."""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.valid_update_form_input = {
            'email': 'bobysmithy@example.org',
            'first_name': 'Bobby',
            'last_name': 'Smithy',
            'bio': 'Hello',
            'chess_experience': 'AV',
            'personal_statement': 'I am not Orangutan',
        }

    def test_form_has_necessary_fields(self):
        """Test if the update user form contains the necessary fields."""

        form = UpdateUserForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('email', form.fields)
        self.assertTrue(isinstance(form.fields['email'], forms.EmailField))
        self.assertIn('bio', form.fields)
        self.assertIn('chess_experience', form.fields)
        self.assertIn('personal_statement', form.fields)

    def test_form_is_valid(self):
        """Test the update user form accepts a valid input."""

        form = UpdateUserForm(data=self.valid_update_form_input)
        self.assertTrue(form.is_valid())

    def test_form_saves_correctly(self):
        """Test if the new profile is updated correctly."""

        user = User.objects.get(email='bobsmith@example.org')

        form = UpdateUserForm(instance=user, data=self.valid_update_form_input)
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

    """ Unit test for email """

    def test_form_rejects_blank_email(self):
        self.valid_update_form_input['email'] = ''
        form = UpdateUserForm(data=self.valid_update_form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_email_without_before_at_symbol(self):
        self.valid_update_form_input['email'] = '@example.org'
        form = UpdateUserForm(data=self.valid_update_form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_email_without_at_symbol(self):
        self.valid_update_form_input['email'] = 'bobysmithyexample.org'
        form = UpdateUserForm(data=self.valid_update_form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_email_that_is_not_unique(self):
        second_person = User.objects.get(email='bethsmith@example.org')
        self.valid_update_form_input['email'] = second_person.email
        form = UpdateUserForm(data=self.valid_update_form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_email_wihout_domain_name(self):
        self.valid_update_form_input['email'] = 'bobysmithy@.org'
        form = UpdateUserForm(data=self.valid_update_form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_email_without_domain(self):
        self.valid_update_form_input['email'] = 'bobysmithy@example'
        form = UpdateUserForm(data=self.valid_update_form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_email_with_more_than_one_at(self):
        self.valid_update_form_input['email'] = 'johndoe@@example.org'
        form = UpdateUserForm(data=self.valid_update_form_input)
        self.assertFalse(form.is_valid())

    """ Unit test for first name """

    def test_form_rejects_first_name_with_more_than_50_characters(self):
        self.valid_update_form_input['first_name'] = 'j' * 51
        form = UpdateUserForm(data=self.valid_update_form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_first_name_with_50_characters(self):
        self.valid_update_form_input['first_name'] = 'j' * 50
        form = UpdateUserForm(data=self.valid_update_form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_first_name(self):
        self.valid_update_form_input['first_name'] = ''
        form = UpdateUserForm(data=self.valid_update_form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_first_name_that_is_not_unique(self):
        second_user = User.objects.get(email='bethsmith@example.org')
        self.valid_update_form_input['first_name'] = second_user.first_name
        form = UpdateUserForm(data=self.valid_update_form_input)
        self.assertTrue(form.is_valid())

    """ Unit test for last name """

    def test_form_rejects_last_name_with_more_than_50_characters(self):
        self.valid_update_form_input['last_name'] = 'j' * 51
        form = UpdateUserForm(data=self.valid_update_form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_last_name_with_50_characters(self):
        self.valid_update_form_input['last_name'] = 'j' * 50
        form = UpdateUserForm(data=self.valid_update_form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_last_name(self):
        self.valid_update_form_input['last_name'] = ''
        form = UpdateUserForm(data=self.valid_update_form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_last_name_that_is_not_unique(self):
        second_user = User.objects.get(email='bethsmith@example.org')
        self.valid_update_form_input['last_name'] = second_user.last_name
        form = UpdateUserForm(data=self.valid_update_form_input)
        self.assertTrue(form.is_valid())

    """ Unit test for bio """

    def test_form_accepts_blank_bio(self):
        self.valid_update_form_input['bio'] = ''
        form = UpdateUserForm(data=self.valid_update_form_input)
        self.assertTrue(form.is_valid())

    def test_form_accepts_bio_that_is_not_unique(self):
        second_user = User.objects.get(email='bethsmith@example.org')
        self.valid_update_form_input['bio'] = second_user.bio
        form = UpdateUserForm(data=self.valid_update_form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_bio_with_more_than_720_characters(self):
        self.valid_update_form_input['bio'] = 'x' * 721
        form = UpdateUserForm(data=self.valid_update_form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_bio_with_720_characters(self):
        self.valid_update_form_input['bio'] = 'x' * 720
        form = UpdateUserForm(data=self.valid_update_form_input)
        self.assertTrue(form.is_valid())

    """ Unit test for chess_experience """

    def test_form_rejects_blank_chess_experience(self):
        self.valid_update_form_input['chess_experience'] = ''
        form = UpdateUserForm(data=self.valid_update_form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_chess_experience_that_is_not_unique(self):
        second_user = User.objects.get(email='bethsmith@example.org')
        self.valid_update_form_input['chess_experience'] = second_user.chess_experience
        form = UpdateUserForm(data=self.valid_update_form_input)
        self.assertTrue(form.is_valid())

    """ Unit test for personal_statement """

    def test_form_accepts_blank_personal_statement(self):
        self.valid_update_form_input['personal_statement'] = ''
        form = UpdateUserForm(data=self.valid_update_form_input)
        self.assertTrue(form.is_valid())

    def test_form_accepts_personal_statement_that_is_not_unique(self):
        second_user = User.objects.get(email='bethsmith@example.org')
        self.valid_update_form_input['personal_statement'] = second_user.personal_statement
        form = UpdateUserForm(data=self.valid_update_form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_personal_statement_with_more_than_720_characters(self):
        self.valid_update_form_input['personal_statement'] = 'x' * 721
        form = UpdateUserForm(data=self.valid_update_form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_personal_statement_with_720_characters(self):
        self.valid_update_form_input['personal_statement'] = 'x' * 720
        form = UpdateUserForm(data=self.valid_update_form_input)
        self.assertTrue(form.is_valid())
