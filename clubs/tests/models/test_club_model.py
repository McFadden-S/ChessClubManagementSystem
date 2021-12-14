"""Unit tests for Club model."""
from clubs.models import Club
from django.core.exceptions import ValidationError
from django.test import TestCase

class ClubModelTestCase(TestCase):
    """Unit tests for Club model."""

    fixtures = [
        'clubs/tests/fixtures/default_club.json',
        'clubs/tests/fixtures/other_clubs.json',
    ]

    def setUp(self):
        self.club = Club.objects.get(name='Flying Orangutans')
        self.second_club = Club.objects.get(name='Flying Orangutans 2')

    def test_valid_club(self):
        self.assert_club_is_valid()

    """ Unit test for name """

    def test_name_is_unique(self):
        self.club.name = self.second_club.name
        self.assert_club_is_invalid()

    def test_name_must_not_be_longer_50_chars(self):
        self.club.name = 'o' * 51
        self.assert_club_is_invalid()

    def test_name_can_have_50_chars(self):
        self.club.name = 'o' * 50
        self.assert_club_is_valid()

    def test_name_must_not_be_blank(self):
        self.club.name = ''
        self.assert_club_is_invalid()

    """ Unit test for description """

    def test_description_cannot_be_blank(self):
        self.club.description = ''
        self.assert_club_is_invalid()

    def test_description_need_not_be_unique(self):
        self.club.description = self.second_club.description
        self.assert_club_is_valid()

    def test_description_must_not_be_longer_500_chars(self):
        self.club.description = 'o' * 501
        self.assert_club_is_invalid()

    def test_description_can_have_500_chars(self):
        self.club.description = 'o' * 500
        self.assert_club_is_valid()

    """ Unit tests for valid address """
    def test_address_must_not_be_blank(self):
        self.club.address = ''
        self.assert_club_is_invalid()

    def test_address_need_not_be_unique(self):
        self.club.address = self.second_club.address
        self.assert_club_is_valid()

    def test_address_must_not_be_longer_100_chars(self):
        self.club.address = 'o' * 101
        self.assert_club_is_invalid()

    def test_address_can_have_100_chars(self):
        self.club.address = 'o' * 100
        self.assert_club_is_valid()



    """ Unit tests for city """

    def test_city_must_not_be_blank(self):
        self.club.city = ''
        self.assert_club_is_invalid()

    def test_city_need_not_be_unique(self):
        self.club.city = self.second_club.city
        self.assert_club_is_valid()

    def test_city_must_not_be_longer_50_chars(self):
        self.club.city = 'o' * 51
        self.assert_club_is_invalid()

    def test_city_can_have_50_chars(self):
        self.club.city = 'o' * 50
        self.assert_club_is_valid()

    """ Unit tests for postal code """

    def test_postal_code_need_not_be_unique(self):
        self.club.postal_code = self.second_club.postal_code
        self.assert_club_is_valid()

    def test_postal_code_must_not_be_blank(self):
        self.club.postal_code = ''
        self.assert_club_is_invalid()

    def test_postal_code_must_not_be_longer_20_chars(self):
        self.club.postal_code = 'o' * 21
        self.assert_club_is_invalid()

    def test_postal_code_can_have_20_chars(self):
        self.club.postal_code = 'o' * 20
        self.assert_club_is_valid()

    """ Unit tests for country """

    def test_country_must_not_be_blank(self):
        self.club.country = ''
        self.assert_club_is_invalid()

    def test_country_need_not_be_unique(self):
        self.club.country = self.second_club.country
        self.assert_club_is_valid()


    def assert_club_is_valid(self):
        try:
            self.club.full_clean()
        except (ValidationError):
            self.fail('Test club needs to be made valid')

    def assert_club_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.club.full_clean()
