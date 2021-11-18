from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import User

class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='johndoe@example.com',
            first_name = 'John',
            last_name = 'Doe',
            bio='Hi',
            chess_experience='AV',
            personal_statement = 'I am John Doe',
            password="Password123"
        )

    def test_valid_user(self):
        self.assert_user_is_valid()


    """ Unit test for email """
    def test_email_must_not_be_blank(self):
        self.user.email = ''
        self.assert_user_is_invalid()

    def test_email_must_have_before_at_symbol(self):
        self.user.email = '@example.com'
        self.assert_user_is_invalid()

    def test_email_must_have_at_symbol(self):
        self.user.email = 'johndoeexample.com'
        self.assert_user_is_invalid()

    def test_email_is_unique(self):
        second_person = self.create_second_person()
        self.user.email = second_person.email
        self.assert_user_is_invalid()

    def test_email_must_include_domain_name(self):
        self.user.email = 'johndoe@.com'
        self.assert_user_is_invalid()

    def test_email_must_include_domain(self):
        self.user.email = 'johndoe@example'
        self.assert_user_is_invalid()



    """ Unit test for first name """
    def test_first_name_must_not_be_longer_50_chars(self):
        self.user.first_name = 'j' * 51
        self.assert_user_is_invalid();

    def test_first_name_can_have_50_chars(self):
        self.user.first_name = 'j' * 50
        self.assert_user_is_valid();

    def test_first_name_must_not_be_blank(self):
        self.user.first_name = ''
        self.assert_user_is_invalid();


    """ Unit test for last name """
    def test_last_name_must_not_be_longer_50_chars(self):
        self.user.first_name = 'j' * 51
        self.assert_user_is_invalid();

    def test_last_name_can_have_50_chars(self):
        self.user.first_name = 'j' * 50
        self.assert_user_is_valid();

    def test_last_name_must_not_be_blank(self):
        self.user.first_name = ''
        self.assert_user_is_invalid();


    """ Unit test for bio """
    def test_bio_could_be_blank(self):
        self.user.bio = ''
        self.assert_user_is_valid();


    """ Unit test for chess_experience """
    def test_chess_experience_must_not_be_blank(self):
        self.user.chess_experience = ''
        self.assert_user_is_invalid();

    def test_chess_experience_does_not_have_to_be_unique(self):
        second_user = self.create_second_person()
        self.user.chess_experience = second_user.chess_experience
        self.assert_user_is_valid();


    """ Unit test for personal_statement """
    def test_personal_statement_could_be_blank(self):
        self.user.personal_statement = ''
        self.assert_user_is_valid();



    def assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user needs to be made valid')

    def assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()

    def create_second_person(self):
        second_person = User.objects.create_user(
            email='janedoe@example.com',
            first_name='Jane',
            last_name='Doe',
            bio='Hi',
            chess_experience='BG',
            personal_statement='I am Jane Doe',
            password="Password123"
        )
        return second_person
