from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import Club

class ClubModelTestCase(TestCase):

    def setUp(self):
        self.club = Club.objects.create(
            name='Orangutan',
            address='Bush House',
            city='London',
            postal_code='WC2B 4BG',
            country='GB',
            location='51.51274545,-0.11717261325662154',
            description='Aim to get the best orangutans out there'
        )
        self.second_club = Club.objects.create(
            name='Monkeys',
            address='Stand Building',
            city='London',
            postal_code='WC2R 2LS',
            country='GB',
            location='51.51274545,-0.11717261325662154',
            description='Aim to get the best monkeys out there'
        )

    def test_valid_club(self):
        self.assert_club_is_valid()

    """ Unit test for name """
    def test_name_is_unique(self):
        self.club.name = self.second_club.name
        self.assert_club_is_invalid()

    def test_name_must_not_be_longer_50_chars(self):
        self.club.name = 'o' * 51
        self.assert_club_is_invalid();

    def test_name_can_have_50_chars(self):
        self.club.name = 'o' * 50
        self.assert_club_is_valid();

    def test_name_must_not_be_blank(self):
        self.club.name = ''
        self.assert_club_is_invalid();

    """ Unit test for description """
    def test_description_cannot_be_blank(self):
        self.club.description = ''
        self.assert_club_is_invalid();



    def assert_club_is_valid(self):
        try:
            self.club.full_clean()
        except (ValidationError):
            self.fail('Test club needs to be made valid')

    def assert_club_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.club.full_clean()
