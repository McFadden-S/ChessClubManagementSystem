from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import Club_Member, User, Club

class ClubMemberTest(TestCase):

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.user = User.objects.get(email='bobsmith@example.org')
        self.club = Club.objects.get(name='Flying Orangutans')
        self.club_member = Club_Member.objects.create(
            user=self.user,
            club=self.club
        )

    def test_valid_club_member(self):
        try:
            self.club_member.full_clean()
        except ValidationError:
            self.fail("Test club member should be valid")

    def test_user_must_not_be_blank(self):
        self.club_member.user = None
        with self.assertRaises(ValidationError):
            self.club_member.full_clean()

    def test_club_must_not_be_blank(self):
        self.club_member.club = None
        with self.assertRaises(ValidationError):
            self.club_member.full_clean()

    # def test_club_name_must_not_be_too_long(self):
    #     self.club.club_name = 'x' * 51
    #     with self.assertRaises(ValidationError):
    #         self.club.full_clean()

    def test_authorization_must_be_valid_choice(self):
        self.club_member.authorization = "XX"
        with self.assertRaises(ValidationError):
            self.club_member.full_clean()

    def test_authorization_must_not_be_blank(self):
        self.club_member.authorization = ""
        with self.assertRaises(ValidationError):
            self.club_member.full_clean()

    def test_unique_surrogate_key(self):
        club2 = Club_Member(user=self.user, authorization='OW')
        with self.assertRaises(ValidationError):
            club2.full_clean()
