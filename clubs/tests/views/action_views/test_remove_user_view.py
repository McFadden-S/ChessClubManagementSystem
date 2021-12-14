"""Unit tests for the remove user view."""
from clubs.models import Club, Club_Member, User
from clubs.tests.helpers import LogInTester,reverse_with_next
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from django.contrib import messages

class RemoveUserViewTestCase(TestCase, LogInTester):
    """Unit tests for the remove user view."""
    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.owner = User.objects.get(email='bobsmith@example.org')
        self.officer = User.objects.get(email='bethsmith@example.org')
        self.another_officer = User.objects.get(email='jamessmith@example.org')
        self.member = User.objects.get(email='johnsmith@example.org')
        self.another_member = User.objects.get(email='marrysmith@example.org')
        self.applicant = User.objects.get(email='harrysmith@example.org')
        self.another_applicant = User.objects.get(email='kellysmith@example.org')
        self.club = Club.objects.get(name='Flying Orangutans')
        Club_Member.objects.create(user=self.owner, authorization='OW', club=self.club)
        Club_Member.objects.create(user=self.officer, authorization='OF', club=self.club)
        Club_Member.objects.create(user=self.another_officer, authorization='OF', club=self.club)
        Club_Member.objects.create(user=self.member, authorization='ME', club=self.club)
        Club_Member.objects.create(user=self.another_member, authorization='ME', club=self.club)
        Club_Member.objects.create(user=self.applicant, authorization='AP', club=self.club)
        Club_Member.objects.create(user=self.another_applicant, authorization='AP', club=self.club)
        self.remove_member_url = reverse('remove_user', kwargs={'club_id': self.club.id, 'user_id': self.member.id})
        self.remove_officer_url = reverse('remove_user', kwargs={'club_id': self.club.id, 'user_id': self.officer.id})

    def test_remove_member_url(self):
        """Test for the remove member url."""

        self.assertEqual(self.remove_member_url,f'/{self.club.id}/remove_user/{self.member.id}')

    def test_remove_officer_url(self):
        """Test for the remove officer url."""

        self.assertEqual(self.remove_officer_url,f'/{self.club.id}/remove_user/{self.officer.id}')

    """ Unit tests for owner successfully removing a user """

    def test_get_owner_remove_member(self):
        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Club_Member.objects.count()
        response = self.client.get(self.remove_member_url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        response_message = self.client.get(redirect_url)
        messages_list = list(response_message.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if the member has been removed
        self.assertEqual(before_count, after_count+1)

        # Checks if the member does not exist in the Club
        with self.assertRaises(ObjectDoesNotExist):
            Club_Member.objects.get(user=self.member, club=self.club)


    def test_get_owner_remove_officer(self):
        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Club_Member.objects.count()
        response = self.client.get(self.remove_officer_url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        response_message = self.client.get(redirect_url)
        messages_list = list(response_message.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if the officer has been removed
        self.assertEqual(before_count, after_count+1)

        # Checks if the officer does not exist in the Club
        with self.assertRaises(ObjectDoesNotExist):
            Club_Member.objects.get(user=self.officer, club=self.club)

    """ Unit tests for owner not being able to remove user """

    def test_get_owner_remove_applicant(self):
        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Club_Member.objects.count()
        self.url = reverse('remove_user', kwargs={'club_id': self.club.id, 'user_id': self.applicant.id})
        response = self.client.get(self.url)
        response_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if no applicant has been removed
        self.assertEqual(before_count, after_count)

        # Checks if the applicant still exists in the Club
        try:
            Club_Member.objects.get(user=self.applicant, club=self.club)
        except (ObjectDoesNotExist):
            self.fail('The user should not be removed')


    def test_get_owner_remove_themselves(self):
        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Club_Member.objects.count()
        self.url = reverse('remove_user', kwargs={'club_id': self.club.id, 'user_id': self.owner.id})
        response = self.client.get(self.url)
        response_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if no owner has been removed
        self.assertEqual(before_count, after_count)

        # Checks if the owner still exists in the Club
        try:
            Club_Member.objects.get(user=self.owner, club=self.club)
        except (ObjectDoesNotExist):
            self.fail('The user should not be removed')

    def test_get_officer_remove_member(self):
        """Test for the officer successfully removing a member."""

        self.client.login(email=self.officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Club_Member.objects.count()
        response = self.client.get(self.remove_member_url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        response_message = self.client.get(redirect_url)
        messages_list = list(response_message.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if the member has been removed
        self.assertEqual(before_count, after_count+1)

        # Checks if the member does not exist in the Club
        with self.assertRaises(ObjectDoesNotExist):
            Club_Member.objects.get(user=self.member, club=self.club)

    """Unit tests for officer not able to remove a user"""

    def test_get_officer_remove_owner(self):
        self.client.login(email=self.officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Club_Member.objects.count()
        self.url = reverse('remove_user', kwargs={'club_id': self.club.id, 'user_id': self.owner.id})
        response = self.client.get(self.url)
        response_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if no owner has been removed
        self.assertEqual(before_count, after_count)

        # Checks if the owner still exists in the Club
        try:
            Club_Member.objects.get(user=self.owner, club=self.club)
        except (ObjectDoesNotExist):
            self.fail('The user should not be removed')


    def test_get_officer_remove_applicant(self):
        self.client.login(email=self.officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Club_Member.objects.count()
        self.url = reverse('remove_user', kwargs={'club_id': self.club.id, 'user_id': self.applicant.id})
        response = self.client.get(self.url)
        response_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if no applicant has been removed
        self.assertEqual(before_count, after_count)

        # Checks if the applicant still exists in the Club
        try:
            Club_Member.objects.get(user=self.applicant, club=self.club)
        except (ObjectDoesNotExist):
            self.fail('The user should not be removed')


    def test_get_officer_remove_themselves(self):
        self.client.login(email=self.officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Club_Member.objects.count()
        response = self.client.get(self.remove_officer_url)
        response_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if no officer has been removed
        self.assertEqual(before_count, after_count)

        # Checks if the officer still exists in the Club
        try:
            Club_Member.objects.get(user=self.officer, club=self.club)
        except (ObjectDoesNotExist):
            self.fail('The user should not be removed')


    def test_get_officer_remove_another_officer(self):
        self.client.login(email=self.officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Club_Member.objects.count()
        self.url = reverse('remove_user', kwargs={'club_id': self.club.id, 'user_id': self.another_officer.id})
        response = self.client.get(self.url)
        response_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if no officer has been removed
        self.assertEqual(before_count, after_count)

        # Checks if the officer still exists in the Club
        try:
            Club_Member.objects.get(user=self.another_officer, club=self.club)
        except (ObjectDoesNotExist):
            self.fail('The user should not be removed')

    """Unit tests for member not able to remove a user"""

    def test_get_member_remove_applicant(self):
        self.client.login(email=self.member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Club_Member.objects.count()
        self.url = reverse('remove_user', kwargs={'club_id': self.club.id, 'user_id': self.applicant.id})
        response = self.client.get(self.url)
        response_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if no applicant has been removed
        self.assertEqual(before_count, after_count)

        # Checks if the applicant still exists in the Club
        try:
            Club_Member.objects.get(user=self.applicant, club=self.club)
        except (ObjectDoesNotExist):
            self.fail('The user should not be removed')


    def test_get_member_remove_officer(self):
        self.client.login(email=self.member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Club_Member.objects.count()
        response = self.client.get(self.remove_officer_url)
        response_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if no officer has been removed
        self.assertEqual(before_count, after_count)

        # Checks if the officer still exists in the Club
        try:
            Club_Member.objects.get(user=self.officer, club=self.club)
        except (ObjectDoesNotExist):
            self.fail('The user should not be removed')


    def test_get_member_remove_owner(self):
        self.client.login(email=self.member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Club_Member.objects.count()
        self.url = reverse('remove_user', kwargs={'club_id': self.club.id, 'user_id': self.owner.id})
        response = self.client.get(self.url)
        response_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if no owner has been removed
        self.assertEqual(before_count, after_count)

        # Checks if the owner still exists in the Club
        try:
            Club_Member.objects.get(user=self.owner, club=self.club)
        except (ObjectDoesNotExist):
            self.fail('The user should not be removed')


    def test_get_member_remove_themselves(self):
        self.client.login(email=self.member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Club_Member.objects.count()
        response = self.client.get(self.remove_member_url)
        response_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if no member has been removed
        self.assertEqual(before_count, after_count)

        # Checks if the member still exists in the Club
        try:
            Club_Member.objects.get(user=self.member, club=self.club)
        except (ObjectDoesNotExist):
            self.fail('The user should not be removed')


    def test_get_member_remove_another_member(self):
        self.client.login(email=self.member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Club_Member.objects.count()
        self.url = reverse('remove_user', kwargs={'club_id': self.club.id, 'user_id': self.another_member.id})
        response = self.client.get(self.url)
        response_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if no member has been removed
        self.assertEqual(before_count, after_count)

        # Checks if the member still exists in the Club
        try:
            Club_Member.objects.get(user=self.another_member, club=self.club)
        except (ObjectDoesNotExist):
            self.fail('The user should not be removed')

    """Unit tests for applicant not able to remove a user"""

    def test_get_applicant_remove_member(self):
        self.client.login(email=self.applicant.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Club_Member.objects.count()
        response = self.client.get(self.remove_member_url)
        response_url = reverse('waiting_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if no member has been removed
        self.assertEqual(before_count, after_count)

        # Checks if the member still exists in the Club
        try:
            Club_Member.objects.get(user=self.member, club=self.club)
        except (ObjectDoesNotExist):
            self.fail('The user should not be removed')


    def test_get_applicant_remove_officer(self):
        self.client.login(email=self.applicant.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Club_Member.objects.count()
        response = self.client.get(self.remove_officer_url)
        response_url = reverse('waiting_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if no officer has been removed
        self.assertEqual(before_count, after_count)

        # Checks if the officer still exists in the Club
        try:
            Club_Member.objects.get(user=self.officer, club=self.club)
        except (ObjectDoesNotExist):
            self.fail('The user should not be removed')


    def test_get_applicant_remove_owner(self):
        self.client.login(email=self.applicant.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Club_Member.objects.count()
        self.url = reverse('remove_user', kwargs={'club_id': self.club.id, 'user_id': self.owner.id})
        response = self.client.get(self.url)
        response_url = reverse('waiting_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if no owner has been removed
        self.assertEqual(before_count, after_count)

        # Checks if the owner still exists in the Club
        try:
            Club_Member.objects.get(user=self.owner, club=self.club)
        except (ObjectDoesNotExist):
            self.fail('The user should not be removed')


    def test_get_applicant_remove_themselves(self):
        self.client.login(email=self.applicant.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Club_Member.objects.count()
        self.url = reverse('remove_user', kwargs={'club_id': self.club.id, 'user_id': self.applicant.id})
        response = self.client.get(self.url)
        response_url = reverse('waiting_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if no applicant has been removed
        self.assertEqual(before_count, after_count)

        # Checks if the applicant still exists in the Club
        try:
            Club_Member.objects.get(user=self.applicant, club=self.club)
        except (ObjectDoesNotExist):
            self.fail('The user should not be removed')


    def test_get_applicant_remove_another_applicant(self):
        self.client.login(email=self.applicant.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Club_Member.objects.count()
        self.url = reverse('remove_user', kwargs={'club_id': self.club.id, 'user_id': self.another_applicant.id})
        response = self.client.get(self.url)
        response_url = reverse('waiting_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if no applicant has been removed
        self.assertEqual(before_count, after_count)

        # Checks if the applicant still exists in the Club
        try:
            Club_Member.objects.get(user=self.another_applicant, club=self.club)
        except (ObjectDoesNotExist):
            self.fail('The user should not be removed')

    """Unit tests for redirecting when not logged in"""

    def test_get_remove_member_redirects_when_not_logged_in(self):
        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.remove_member_url)
        redirect_url = reverse_with_next('log_in', self.remove_member_url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_remove_officer_redirects_when_not_logged_in(self):
        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.remove_officer_url)
        redirect_url = reverse_with_next('log_in', self.remove_officer_url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
