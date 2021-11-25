from django.test import TestCase
from clubs.models import Club
from clubs.forms import CreateClubForm
from django import forms

class CreateClubFormTestCase(TestCase):
    def setUp(self):
        self.valid_form_input = {
            'name': 'Orangutan',
            'address': 'Bush House',
            'city': 'London',
            'postal_code': 'WC2B 4BG',
            'country': 'GB',
            'description' : 'Aim to get the best orangutans out there'
        }

    def test_a_valid_create_club_form(self):
        form = CreateClubForm(data=self.valid_form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = CreateClubForm()
        self.assertIn('name', form.fields)
        self.assertIn('address', form.fields)
        self.assertIn('city', form.fields)
        self.assertIn('postal_code', form.fields)
        self.assertIn('country', form.fields)
        self.assertIn('description', form.fields)

    def test_form_must_save_correctly(self):
        form = CreateClubForm(data=self.valid_form_input)
        before_count = Club.objects.count()
        form.save()
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count+1)

        club = Club.objects.get(name='Orangutan')
        self.assertEqual(club.name, 'Orangutan')
        self.assertEqual(club.address, 'Bush House')
        self.assertEqual(club.city, 'London')
        self.assertEqual(club.postal_code, 'WC2B 4BG')
        self.assertEqual(club.country, 'GB')
        self.assertEqual(club.description, 'Aim to get the best orangutans out there')
