from django.test import TestCase
from clubs.models import User, Club_Member, Club
from clubs.forms import CreateClubForm
from django.urls import reverse

class CreateClubViewTestCase(TestCase):
    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        # Applicant cannot create club
        self.user = User.objects.get(email='bobsmith@example.org')
        self.secondary_user = User.objects.get(email='bethsmith@example.org')
        Club_Member.objects.create(
            user=self.user, authorization='ME'
        )
        Club_Member.objects.create(
            user=self.secondary_user, authorization='AP'
        )
        self.valid_form_input = {
            'name': 'Orangutan',
            'address': 'Bush House',
            'city': 'London',
            'postal_code': 'WC2B 4BG',
            'country': 'GB',
            'description' : 'Aim to get the best orangutans out there'
        }
        self.url = reverse('create_club')

    def test_get_create_club(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_club.html')
        form = response.context['form']
        self.assertTrue(isinstance(form,CreateClubForm))
        self.assertEqual(form.is_bound, False)

    def test_get_create_club_by_applicant(self):
        self.client.login(email=self.secondary_user.email, password='Password123')
        response = self.client.get(self.url)
        redirect_url=reverse('waiting_list')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    # No need if using client validation
    # def test_unsuccesful_sign_up(self):

    def test_succesful_create_club(self):
         # SAVE TO CLUB DB
        self.client.login(email=self.user.email, password='Password123')
        before_count = Club.objects.count()
        response = self.client.post(self.url, self.valid_form_input, follow=True)
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count+1)

        # SAVE TO CLUB DB
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count+1)

        # TEST 2 - REDIRECT SUCCESSFUL - currenly members_list but should be club home page
        response_url = reverse('members_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'members_list.html')

        #test 4 - IN DB SEE NEW USER
        club = Club.objects.get(name='Orangutan')
        self.assertEqual(club.name, 'Orangutan')
        self.assertEqual(club.address, 'Bush House')
        self.assertEqual(club.city, 'London')
        self.assertEqual(club.postal_code, 'WC2B 4BG')
        self.assertEqual(club.country, 'GB')
        self.assertEqual(club.description, 'Aim to get the best orangutans out there')
        messages_list = list(response.context['messages'])
        # should change to 1 after add message
        self.assertEqual(len(messages_list), 0)