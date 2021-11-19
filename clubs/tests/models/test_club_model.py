from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import Club, User

class ClubTest(TestCase):

    fixtures = ['clubs/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(email='bobsmith@example.org')
        self.club = Club.objects.create(
            user=self.user
        )

    def test_valid_club(self):
        try:
            self.club.full_clean()
        except ValidationError:
            self.fail("Test club should be valid")

    def test_user_must_not_be_blank(self):
        self.club.user = None
        with self.assertRaises(ValidationError):
            self.club.full_clean()

    def test_club_must_not_be_blank(self):
        self.club.club_name = ''
        with self.assertRaises(ValidationError):
            self.club.full_clean()

    def test_club_name_must_not_be_too_long(self):
        self.club.club_name = 'x' * 51
        with self.assertRaises(ValidationError):
            self.club.full_clean()

    def test_authorization_must_be_valid_choice(self):
        self.club.authorization = "XX"
        with self.assertRaises(ValidationError):
            self.club.full_clean()

    def test_authorization_must_not_be_blank(self):
        self.club.authorization = ""
        with self.assertRaises(ValidationError):
            self.club.full_clean()

    def test_unique_surrogate_key(self):
        club2 = Club(user=self.user, authorization='OW')
        with self.assertRaises(ValidationError):
            club2.full_clean()
