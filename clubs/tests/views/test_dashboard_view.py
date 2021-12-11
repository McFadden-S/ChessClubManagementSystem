from django.test import TestCase
from clubs.models import Club, User, Club_Member
from django.urls import reverse
from clubs.tests.helpers import reverse_with_next
from django.contrib.auth.hashers import check_password
from clubs.tests.helpers import LogInTester


# Used this from clucker project with some modifications
class MembersListViewTestCase(TestCase, LogInTester):
    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json',
    ]

    def setUp(self):
        self.user = User.objects.get(email='bobsmith@example.org')
        self.secondary_user = User.objects.get(email='bethsmith@example.org')
        self.tertiary_user = User.objects.get(email='johnsmith@example.org')
        self.club = Club.objects.create(
            name='club1',
            address='Bush House',
            city='London',
            postal_code='WC2B 4BG	',
            country='United Kingdom',
            description='Bush House',
        )
        self.club_member = Club_Member.objects.create(
            user=self.user,
            club=self.club,
            authorization='OW',
        )
        self.club2 = Club.objects.create(
            # Broad St, Oxford OX1 3BG
            name='club2',
            address='Broad St',
            city='Oxford',
            postal_code='OX1 3BG	',
            country='United Kingdom',
            description='Bodleian Library',
        )
        self.club_member2 = Club_Member.objects.create(
            user=self.secondary_user,
            club=self.club2,
            authorization='OW',
        )
        self.club3 = Club.objects.create(
            # The Old Schools, Trinity Ln, Cambridge CB2 1TN
            name='club3',
            address='Trinity Ln',
            city='Cambridge',
            postal_code='CB2 1TN	',
            country='United Kingdom',
            description='The Old Schools',
        )
        self.club_member3 = Club_Member.objects.create(
            user=self.tertiary_user,
            club=self.club3,
            authorization='OW',
        )

        self.url = reverse('dashboard')

    def create_ordered_list_by(self, order_by_var):
        club_list = Club.objects.all()
        sorted_list = Club.objects.filter(id__in=club_list).order_by(order_by_var)
        return sorted_list

    def test_members_list_url(self):
        self.assertEqual(self.url, '/dashboard/')

    def test_get_clubs_list(self):
        self.client.login(email=self.user.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_get_dashboard_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertFalse(self._is_logged_in())


    # TODO Refactor tests to reflect javascript search/sort
    # def test_search_bar_to_filter_list(self):
    #     self.client.login(email=self.user.email, password='Password123')
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'dashboard.html')
    #     self.assertContains(response, 'club1')
    #     self.assertContains(response, 'club2')
    #     self.assertContains(response, 'club3')
    #     search_bar = 'club1'
    #     response = self.client.post(self.url, {'search_btn': True, 'searched_letters': search_bar})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'dashboard.html')
    #     self.assertContains(response, 'club1')
    #     self.assertNotContains(response, 'club2')
    #     self.assertNotContains(response, 'club3')
    #
    # def test_empty_search_bar(self):
    #     self.client.login(email=self.user.email, password='Password123')
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'dashboard.html')
    #     self.assertContains(response, 'club1')
    #     self.assertContains(response, 'club2')
    #     self.assertContains(response, 'club3')
    #     search_bar = ''
    #     response = self.client.post(self.url, {'search_btn': True, 'searched_letters': search_bar})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'dashboard.html')
    #     self.assertContains(response, 'club1')
    #     self.assertContains(response, 'club2')
    #     self.assertContains(response, 'club3')
    #
    # def test_sorted_list_club_name(self):
    #     sort_table = 'name'
    #     second_list = list(self.create_ordered_list_by(sort_table))
    #     self.client.login(email=self.user.email, password='Password123')
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'dashboard.html')
    #     response = self.client.post(self.url, {'sort_table': sort_table})
    #     club_list = Club.objects.all()
    #     clubs = list(Club.objects.all().filter(id__in=club_list))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'dashboard.html')
    #     self.assertListEqual(clubs, second_list)
