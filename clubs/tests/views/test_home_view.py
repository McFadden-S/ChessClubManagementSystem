"""Tests of the home view."""
from django.test import TestCase
from clubs.models import User,Club_Member

from django.urls import reverse

class HomeViewTestCase(TestCase):
    """Tests of the home view."""
    fixtures = [
    'clubs/tests/fixtures/default_user.json',]

    def setUp(self):
        self.url = reverse('home')
        self.user = User.objects.get(email='bobsmith@example.org')


    def test_get_home_page(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'home.html')
        self.assertEqual(response.status_code, 200)

    def test_home_url(self):
        self.assertEqual(self.url,'/')

    def test_get_home_redirects_when_logged_in(self):
        club = Club_Member.objects.create(user=self.user)
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('members_list')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'members_list.html')
