"""Unit tests for user model."""
from clubs.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase


class UserModelTestCase(TestCase):
    """Unit tests for user model."""
    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(email='bobsmith@example.org')
        self.superuser = User.objects.create_superuser(
            first_name="Bob",
            last_name="Smith",
            email="email@gmail.com",
            password="Password123",
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

    def test_valid_user(self):
        self.assert_user_is_valid()

    """ Unit test for email """

    def test_email_must_not_be_blank(self):
        self.user.email = ''
        self.assert_user_is_invalid()

    def test_email_must_have_before_at_symbol(self):
        self.user.email = '@example.org'
        self.assert_user_is_invalid()

    def test_email_must_have_at_symbol(self):
        self.user.email = 'bobsmithexample.org'
        self.assert_user_is_invalid()

    def test_email_is_unique(self):
        second_person = User.objects.get(email='bethsmith@example.org')
        self.user.email = second_person.email
        self.assert_user_is_invalid()

    def test_email_must_include_domain_name(self):
        self.user.email = 'bobsmith@.org'
        self.assert_user_is_invalid()

    def test_email_must_include_domain(self):
        self.user.email = 'bobsmith@example'
        self.assert_user_is_invalid()

    def test_email_must_not_contain_more_than_one_at(self):
        self.user.email = 'johndoe@@example.org'
        self.assert_user_is_invalid()
    
    def test_email_must_not_be_none(self):
        with self.assertRaises(TypeError):
            self.newuser = User.objects.create_user(
                first_name="Bob",
                last_name="Smith",
                email=None,
                password="Password123",
            )

    """ Unit test for first name """

    def test_first_name_must_not_be_longer_50_characters(self):
        self.user.first_name = 'j' * 51
        self.assert_user_is_invalid()

    def test_first_name_can_have_50_characters(self):
        self.user.first_name = 'j' * 50
        self.assert_user_is_valid()

    def test_first_name_must_not_be_blank(self):
        self.user.first_name = ''
        self.assert_user_is_invalid()

    def test_first_name_need_not_be_unique(self):
        second_user = User.objects.get(email='bobjone@example.org')
        self.user.first_name = second_user.first_name
        self.assert_user_is_valid()

    """ Unit test for last name """

    def test_last_name_must_not_be_longer_50_chars(self):
        self.user.first_name = 'j' * 51
        self.assert_user_is_invalid()

    def test_last_name_can_have_50_chars(self):
        self.user.first_name = 'j' * 50
        self.assert_user_is_valid()

    def test_last_name_must_not_be_blank(self):
        self.user.first_name = ''
        self.assert_user_is_invalid()

    def test_last_name_need_not_be_unique(self):
        second_user = User.objects.get(email='harrysmith@example.org')
        self.user.last_name = second_user.last_name
        self.assert_user_is_valid()

    """ Unit test for bio """

    def test_bio_could_be_blank(self):
        self.user.bio = ''
        self.assert_user_is_valid()

    def test_bio_need_not_be_unique(self):
        second_user = User.objects.get(email='harrysmith@example.org')
        self.user.bio = second_user.bio
        self.assert_user_is_valid()

    def test_bio_may_contain_720_characters(self):
        self.user.bio = 'x' * 720
        self.assert_user_is_valid()

    def test_bio_must_not_contain_more_than_720_characters(self):
        self.user.bio = 'x' * 721
        self.assert_user_is_invalid()

    """ Unit test for chess_experience """

    def test_chess_experience_must_not_be_blank(self):
        self.user.chess_experience = ''
        self.assert_user_is_invalid()

    def test_chess_experience_does_not_have_to_be_unique(self):
        second_user = User.objects.get(email='bethsmith@example.org')
        self.user.chess_experience = second_user.chess_experience
        self.assert_user_is_valid()

    """ Unit test for personal_statement """

    def test_personal_statement_could_be_blank(self):
        self.user.personal_statement = ''
        self.assert_user_is_valid()

    def test_personal_statement_need_not_be_unique(self):
        second_user = User.objects.get(email='harrysmith@example.org')
        self.user.personal_statement = second_user.personal_statement
        self.assert_user_is_valid()

    def test_personal_statement_may_contain_720_characters(self):
        self.user.bio = 'x' * 720
        self.assert_user_is_valid()

    def test_personal_statement_must_not_contain_more_than_720_characters(self):
        self.user.bio = 'x' * 721
        self.assert_user_is_invalid()

    """valid and invalid user"""

    def assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user needs to be made valid')

    def assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()

    """ –––––––––––––––––––––––––––––––––––––––––– """
    """ –––––––– Unit tests for superuser –––––––– """
    """ –––––––––––––––––––––––––––––––––––––––––– """

    def test_valid_superuser(self):
        self.assert_superuser_is_valid()

    """ Unit test for superuser email """

    def test_email_must_not_be_blank_superuser(self):
        self.superuser.email = ''
        self.assert_superuser_is_invalid()

    def test_email_must_have_before_at_symbol_superuser(self):
        self.superuser.email = '@example.org'
        self.assert_superuser_is_invalid()

    def test_email_must_have_at_symbol_superuser(self):
        self.superuser.email = 'emailgmail.com'
        self.assert_superuser_is_invalid()

    def test_email_is_unique_superuser(self):
        second_person = User.objects.get(email='bethsmith@example.org')
        self.superuser.email = second_person.email
        self.assert_superuser_is_invalid()

    def test_is_staff_false(self):
        with self.assertRaises(ValueError):
            self.superuser = User.objects.create_superuser(
                first_name="Bob",
                last_name="Smith",
                email="email@gmail.com",
                password="Password123",
                is_staff=False,
                is_superuser=True,
                is_active=True,
            )

    def test_is_superuser_false(self):
        with self.assertRaises(ValueError):
            self.superuser = User.objects.create_superuser(
                first_name="Bob",
                last_name="Smith",
                email="email@gmail.com",
                password="Password123",
                is_staff=True,
                is_superuser=False,
                is_active=True,
            )

    def assert_superuser_is_valid(self):
        try:
            self.superuser.full_clean()
        except (ValidationError):
            self.fail('Test user needs to be made valid')

    def assert_superuser_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.superuser.full_clean()