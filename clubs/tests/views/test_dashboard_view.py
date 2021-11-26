from django.test import TestCase
from clubs.models import Club, User, Club_Member
from django.urls import reverse
from clubs.tests.helpers import reverse_with_next
from django.contrib.auth.hashers import check_password


# Used this from clucker project with some modifications
class membersListViewTestCase(TestCase):
    fixtures = [
        'clubs/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(email='bobsmith@example.org')
        self.club1 = Club.objects.create(
            name='club1',
            address = 'Bush House',
            city = 'London',
            postal_code = 'WC2B 4BG	',
            country = 'United Kingdom',
            location = '51.51274545,-0.11717261325662154',
            description = 'Bush House',
        )
        self.club2 = Club.objects.create(
            name='club2',
            address = 'Strand Building',
            city = 'London',
            postal_code = 'WC2B 4BG	',
            country = 'United Kingdom',
            location = '51.51274545,-0.11717261325662154',
            description = 'Strand Building',
        )
        self.club1_member = Club_Member.objects.create(
            user=self.user, authorization='OW'
        )
        self.url = reverse('dashboard')

    def test_members_list_url(self):
        self.assertEqual(self.url, '/dashboard/')

    def test_get_clubs_list(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_get_dashboard_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)


    # TODO Once Log In redirects to another view members only decorator and this test can be UNCOMMENTED
    # def test_get_members_list_redirects_when_applicant(self):
    #     self.client.login(email=self.user.email, password='Password123')
    #     self.club.authorization='AP'
    #     redirect_url = reverse_with_next('home', self.url)
    #     response = self.client.get(self.url)
    #     self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
