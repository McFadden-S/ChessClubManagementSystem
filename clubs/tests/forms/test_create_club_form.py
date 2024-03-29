"""Unit tests for the create club form."""
from clubs.forms import CreateClubForm
from clubs.models import Club
from django.test import TestCase


class CreateClubFormTestCase(TestCase):
    """Unit tests for the create club form."""

    def setUp(self):
        self.valid_form_input = {
            'name': 'Orangutan',
            'address': 'Bush House',
            'city': 'London',
            'postal_code': 'WC2B 4BG',
            'country': 'GB',
            'description': 'Aim to get the best orangutans out there'
        }

    def test_a_valid_create_club_form(self):
        """Test the form to create a valid club"""

        form = CreateClubForm(data=self.valid_form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        """Test the form to check if it has necessary fields"""

        form = CreateClubForm()
        self.assertIn('name', form.fields)
        self.assertIn('address', form.fields)
        self.assertIn('city', form.fields)
        self.assertIn('postal_code', form.fields)
        self.assertIn('country', form.fields)
        self.assertIn('description', form.fields)

    def test_form_must_save_correctly(self):
        """Test that the form must save correctly"""

        form = CreateClubForm(data=self.valid_form_input)
        before_count = Club.objects.count()
        form.save()
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count + 1)

        club = Club.objects.get(name='Orangutan')
        self.assertEqual(club.name, 'Orangutan')
        self.assertEqual(club.address, 'Bush House')
        self.assertEqual(club.city, 'London')
        self.assertEqual(club.postal_code, 'WC2B 4BG')
        self.assertEqual(club.country, 'GB')
        self.assertEqual(club.description, 'Aim to get the best orangutans out there')

    """Negative tests"""

    def test_form_must_not_save_correctly_bad_address(self):
        self.valid_form_input['address'] = "badadress"
        form = CreateClubForm(data=self.valid_form_input)
        before_count = Club.objects.count()
        # assume for now form is valid may need to add validators to forms.py
        with self.assertRaises(IndexError):
            form.save()
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count)

    def test_form_must_not_save_correctly_bad_city(self):
        self.valid_form_input['address'] = "badcity"
        form = CreateClubForm(data=self.valid_form_input)
        before_count = Club.objects.count()
        # assume for now form is valid may need to add validators to forms.py
        with self.assertRaises(IndexError):
            form.save()
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count)

    def test_form_must_not_save_correctly_bad_postalcode(self):
        self.valid_form_input['address'] = "badpostalcode"
        form = CreateClubForm(data=self.valid_form_input)
        before_count = Club.objects.count()
        # assume for now form is valid may need to add validators to forms.py
        with self.assertRaises(IndexError):
            form.save()
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count)

    def test_form_must_not_save_correctly_bad_country(self):
        self.valid_form_input['address'] = "badcountry"
        form = CreateClubForm(data=self.valid_form_input)
        before_count = Club.objects.count()
        # assume for now form is valid may need to add validators to forms.py
        with self.assertRaises(IndexError):
            form.save()
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count)
