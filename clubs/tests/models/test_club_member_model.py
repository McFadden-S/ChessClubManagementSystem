"""Unit tests for Club_Member model."""
from clubs.models import Club, Club_Member, User
from django.core.exceptions import ValidationError
from django.test import TestCase

class ClubMemberTest(TestCase):
    """Unit tests for Club_Member model."""

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
        """Test that the club member's field are correct."""

        try:
            self.club_member.full_clean()
        except ValidationError:
            self.fail("Test club member should be valid")

    def test_user_must_not_be_blank(self):
        """Test for the user that must not be blank."""

        self.club_member.user = None
        with self.assertRaises(ValidationError):
            self.club_member.full_clean()

    def test_club_must_not_be_blank(self):
        """Test for the club that must not be blank."""

        self.club_member.club = None
        with self.assertRaises(ValidationError):
            self.club_member.full_clean()

    def test_authorization_must_be_valid_choice(self):
        """Test that the authorization must be from the choices available."""

        self.club_member.authorization = "XX"
        with self.assertRaises(ValidationError):
            self.club_member.full_clean()

    def test_authorization_must_not_be_blank(self):
        """Test for the authorization that must not be blank."""

        self.club_member.authorization = ""
        with self.assertRaises(ValidationError):
            self.club_member.full_clean()
