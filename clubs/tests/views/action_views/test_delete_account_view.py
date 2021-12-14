"""Unit tests for the delete account view."""
from clubs.models import Club, Club_Member, User
from clubs.tests.helpers import LogInTester, NavbarTesterMixin, reverse_with_next
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse

class DeleteAccountViewTestCase(TestCase, LogInTester, NavbarTesterMixin):
    """Unit tests for the delete account view."""
    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.club = Club.objects.get(name='Flying Orangutans')
        self.owner = User.objects.get(email='bobsmith@example.org')
        self.member = User.objects.get(email="kellysmith@example.org")
        self.user = User.objects.get(email='bethsmith@example.org')
        self.club_owner = Club_Member.objects.create(
            user=self.owner, authorization='OW', club=self.club
        )
        self.secondary_user = User.objects.get(email='harrysmith@example.org')
        self.url = reverse('delete_account')

    def test_delete_account_url(self):
        """Test delete account url """

        self.assertEqual(self.url,'/delete_account/')

    def test_get_delete_account_redirects_when_not_logged_in(self):
        """Test for redirecting user when not logged in."""

        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertFalse(self._is_logged_in())

    def test_any_user_without_club_can_delete_account(self):
        """Test delete account for user without club"""

        self.client.login(email=self.user.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count_user = User.objects.count()
        response = self.client.get(self.url)
        response_message = self.client.get(reverse('home'))
        messages_list = list(response_message.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        after_count_user = User.objects.count()
        self.assertEqual(after_count_user, before_count_user-1)
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)

    """Unit tests for users in club with different authorizations can delete account"""

    def test_applicant_in_club_can_delete_account(self):
        self.client.login(email=self.user.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        club_applicant = Club_Member.objects.create(
            user=self.user,
            authorization='AP',
            club=self.club
        )
        before_count_user = User.objects.count()
        before_count_club_member = Club_Member.objects.count()
        before_count_club = Club.objects.count()
        response = self.client.get(self.url)
        response_message = self.client.get(reverse('home'))
        messages_list = list(response_message.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        after_count_user = User.objects.count()
        after_count_club_member = Club_Member.objects.count()
        after_count_club = Club.objects.count()
        self.assertEqual(after_count_user, before_count_user-1)
        self.assertEqual(after_count_club_member, before_count_club_member-1)
        self.assertEqual(after_count_club, before_count_club)
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)

    def test_member_in_club_can_delete_account(self):
        self.client.login(email=self.user.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        club_member = Club_Member.objects.create(
            user=self.user,
            authorization='ME',
            club=self.club
        )
        before_count_user = User.objects.count()
        before_count_club_member = Club_Member.objects.count()
        before_count_club = Club.objects.count()
        response = self.client.get(self.url)
        response_message = self.client.get(reverse('home'))
        messages_list = list(response_message.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        after_count_user = User.objects.count()
        after_count_club_member = Club_Member.objects.count()
        after_count_club = Club.objects.count()
        self.assertEqual(after_count_user, before_count_user-1)
        self.assertEqual(after_count_club_member, before_count_club_member-1)
        self.assertEqual(after_count_club, before_count_club)
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)

    def test_officer_in_club_can_delete_account(self):
        self.client.login(email=self.user.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        club_officer = Club_Member.objects.create(
            user=self.user,
            authorization='OF',
            club=self.club
        )
        before_count_user = User.objects.count()
        before_count_club_member = Club_Member.objects.count()
        before_count_club = Club.objects.count()
        response = self.client.get(self.url)
        response_message = self.client.get(reverse('home'))
        messages_list = list(response_message.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        after_count_user = User.objects.count()
        after_count_club_member = Club_Member.objects.count()
        after_count_club = Club.objects.count()
        self.assertEqual(after_count_user, before_count_user-1)
        self.assertEqual(after_count_club_member, before_count_club_member-1)
        self.assertEqual(after_count_club, before_count_club)
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)

    def test_owner_who_is_only_person_in_club_can_delete_account(self):
        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count_user = User.objects.count()
        before_count_club_member = Club_Member.objects.count()
        before_count_club = Club.objects.count()
        response = self.client.get(self.url)
        response_message = self.client.get(reverse('home'))
        messages_list = list(response_message.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        after_count_user = User.objects.count()
        after_count_club_member = Club_Member.objects.count()
        after_count_club = Club.objects.count()
        self.assertEqual(after_count_user, before_count_user-1)
        self.assertEqual(after_count_club_member, before_count_club_member-1)
        self.assertEqual(after_count_club, before_count_club-1)
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)

    def test_owner_who_only_has_applicants_in_club_can_delete_account(self):
        """ Test for owner with only applicant in club"""

        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        club_applicant = Club_Member.objects.create(
            user=self.user,
            authorization='AP',
            club=self.club
        )
        before_count_user = User.objects.count()
        before_count_club_member = Club_Member.objects.count()
        before_count_club = Club.objects.count()
        response = self.client.get(self.url)
        response_message = self.client.get(reverse('home'))
        messages_list = list(response_message.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        after_count_user = User.objects.count()
        after_count_club_member = Club_Member.objects.count()
        after_count_club = Club.objects.count()
        self.assertEqual(after_count_user, before_count_user-1)
        self.assertEqual(after_count_club_member, before_count_club_member-2)
        self.assertEqual(after_count_club, before_count_club-1)
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)

    """Unit tests for owner who must transfer ownership before deleting account"""

    def test_owner_who_has_only_has_member_in_club_must_transfer_ownership(self):
        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        club_member = Club_Member.objects.create(
            user=self.member,
            authorization='ME',
            club=self.club
        )
        before_count_user = User.objects.count()
        before_count_club_member = Club_Member.objects.count()
        before_count_club = Club.objects.count()
        response = self.client.get(self.url)
        after_count_user = User.objects.count()
        after_count_club_member = Club_Member.objects.count()
        after_count_club = Club.objects.count()
        self.assertEqual(after_count_user, before_count_user)
        self.assertEqual(after_count_club_member, before_count_club_member)
        # Since club still has member the club still exists
        self.assertEqual(after_count_club, before_count_club)
        response_message = self.client.get(reverse('members_list', kwargs={'club_id' : self.club.id}))
        messages_list = list(response_message.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)
        self.assertRedirects(response, reverse('members_list', kwargs={'club_id' : self.club.id}), status_code=302, target_status_code=200)
        #Owner promotes member to officer
        url_transfer = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': self.member.id})
        self.client.get(url_transfer)
        #Owner transfers ownership from officer to owner
        url_transfer = reverse('transfer_ownership', kwargs={'club_id': self.club.id, 'member_id': self.member.id})
        self.client.get(url_transfer)
        #Original owner now deletes account
        self.client.get(self.url)
        response_message = self.client.get(reverse('home'))
        messages_list = list(response_message.context['messages'])
        # 3 messages for promoting, transferring and deleting account
        self.assertEqual(len(messages_list), 3)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        after_count_user = User.objects.count()
        after_count_club_member = Club_Member.objects.count()
        after_count_club = Club.objects.count()
        self.assertEqual(after_count_user, before_count_user-1)
        self.assertEqual(after_count_club_member, before_count_club_member-1)
        self.assertEqual(after_count_club, before_count_club)

    def test_owner_who_has_only_officer_in_club_must_transfer_ownership(self):
        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        club_officer = Club_Member.objects.create(
            user=self.user,
            authorization='OF',
            club=self.club
        )
        before_count_user = User.objects.count()
        before_count_club_member = Club_Member.objects.count()
        before_count_club = Club.objects.count()
        response = self.client.get(self.url)
        after_count_user = User.objects.count()
        after_count_club_member = Club_Member.objects.count()
        after_count_club = Club.objects.count()
        self.assertEqual(after_count_user, before_count_user)
        self.assertEqual(after_count_club_member, before_count_club_member)
        # Since club still has member the club still exists
        self.assertEqual(after_count_club, before_count_club)
        response_message = self.client.get(reverse('members_list', kwargs={'club_id' : self.club.id}))
        messages_list = list(response_message.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)
        self.assertRedirects(response, reverse('members_list', kwargs={'club_id' : self.club.id}), status_code=302, target_status_code=200)
        #Owner transfers ownership from officer to owner
        url_transfer = reverse('transfer_ownership', kwargs={'club_id': self.club.id, 'member_id': club_officer.id})
        self.client.get(url_transfer)
        #Original owner now deletes account
        self.client.get(self.url)
        response_message = self.client.get(reverse('home'))
        messages_list = list(response_message.context['messages'])
        self.assertEqual(len(messages_list), 2)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        after_count_user = User.objects.count()
        after_count_club_member = Club_Member.objects.count()
        after_count_club = Club.objects.count()
        self.assertEqual(after_count_user, before_count_user-1)
        self.assertEqual(after_count_club_member, before_count_club_member-1)
        self.assertEqual(after_count_club, before_count_club)

    def test_owner_who_has_applicant_and_officer_in_club_must_transfer_ownership(self):
        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())

        club_applicant = Club_Member.objects.create(
            user=self.secondary_user, authorization='AP', club=self.club
        )
        club_officer = Club_Member.objects.create(
            user=self.user, authorization='OF', club=self.club
        )
        before_count_user = User.objects.count()
        before_count_club_member = Club_Member.objects.count()
        before_count_club = Club.objects.count()
        response = self.client.get(self.url)
        after_count_user = User.objects.count()
        after_count_club_member = Club_Member.objects.count()
        after_count_club = Club.objects.count()
        self.assertEqual(after_count_user, before_count_user)
        self.assertEqual(after_count_club_member, before_count_club_member)
        # Since club still has member the club still exists
        self.assertEqual(after_count_club, before_count_club)
        response_message = self.client.get(reverse('members_list', kwargs={'club_id' : self.club.id}))
        messages_list = list(response_message.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)
        self.assertRedirects(response, reverse('members_list', kwargs={'club_id' : self.club.id}), status_code=302, target_status_code=200)
        #Owner transfers ownership from officer to owner
        url_transfer = reverse('transfer_ownership', kwargs={'club_id': self.club.id, 'member_id': User.objects.get(email='bethsmith@example.org').id})
        self.client.get(url_transfer)
        #Original owner now deletes account
        self.client.get(self.url)
        response_message = self.client.get(reverse('home'))
        messages_list = list(response_message.context['messages'])
        self.assertEqual(len(messages_list), 2)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        after_count_user = User.objects.count()
        after_count_club_member = Club_Member.objects.count()
        after_count_club = Club.objects.count()
        self.assertEqual(after_count_user, before_count_user-1)
        self.assertEqual(after_count_club_member, before_count_club_member-1)
        self.assertEqual(after_count_club, before_count_club)

    def test_owner_who_has_applicant_and_member_in_club_must_transfer_ownership(self):
        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        club_applicant = Club_Member.objects.create(
            user=self.secondary_user,
            authorization='AP',
            club=self.club
        )

        club_member = Club_Member.objects.create(
            user=self.user,
            authorization='ME',
            club=self.club
        )
        before_count_user = User.objects.count()
        before_count_club_member = Club_Member.objects.count()
        before_count_club = Club.objects.count()
        response = self.client.get(self.url)
        after_count_user = User.objects.count()
        after_count_club_member = Club_Member.objects.count()
        after_count_club = Club.objects.count()
        self.assertEqual(after_count_user, before_count_user)
        self.assertEqual(after_count_club_member, before_count_club_member)
        # Since club still has member the club still exists
        self.assertEqual(after_count_club, before_count_club)
        response_message = self.client.get(reverse('members_list', kwargs={'club_id' : self.club.id}))
        messages_list = list(response_message.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)
        self.assertRedirects(response, reverse('members_list', kwargs={'club_id' : self.club.id}), status_code=302, target_status_code=200)
        #Owner promotes member to officer
        url_transfer = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': User.objects.get(email='bethsmith@example.org').id})
        self.client.get(url_transfer)
        #Owner transfers ownership from officer to owner
        url_transfer = reverse('transfer_ownership', kwargs={'club_id': self.club.id, 'member_id': User.objects.get(email='bethsmith@example.org').id})
        self.client.get(url_transfer)
        #Original owner now deletes account
        self.client.get(self.url)
        response_message = self.client.get(reverse('home'))
        messages_list = list(response_message.context['messages'])
        # 3 messages for promoting, transferring and deleting account
        self.assertEqual(len(messages_list), 3)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        after_count_user = User.objects.count()
        after_count_club_member = Club_Member.objects.count()
        after_count_club = Club.objects.count()
        self.assertEqual(after_count_user, before_count_user-1)
        self.assertEqual(after_count_club_member, before_count_club_member-1)
        self.assertEqual(after_count_club, before_count_club)

    def test_owner_who_has_officer_and_member_in_club_must_transfer_ownership(self):
        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        club_member = Club_Member.objects.create(
            user=self.secondary_user,
            authorization='ME',
            club=self.club
        )

        club_officer = Club_Member.objects.create(
            user=self.user,
            authorization='OF',
            club=self.club
        )
        before_count_user = User.objects.count()
        before_count_club_member = Club_Member.objects.count()
        before_count_club = Club.objects.count()
        response = self.client.get(self.url)
        after_count_user = User.objects.count()
        after_count_club_member = Club_Member.objects.count()
        after_count_club = Club.objects.count()
        self.assertEqual(after_count_user, before_count_user)
        self.assertEqual(after_count_club_member, before_count_club_member)
        # Since club still has member the club still exists
        self.assertEqual(after_count_club, before_count_club)
        response_message = self.client.get(reverse('members_list', kwargs={'club_id' : self.club.id}))
        messages_list = list(response_message.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)
        self.assertRedirects(response, reverse('members_list', kwargs={'club_id' : self.club.id}), status_code=302, target_status_code=200)
        #Owner transfers ownership from officer to owner
        url_transfer = reverse('transfer_ownership', kwargs={'club_id': self.club.id, 'member_id': User.objects.get(email='bethsmith@example.org').id})
        self.client.get(url_transfer)
        #Original owner now deletes account
        self.client.get(self.url)
        response_message = self.client.get(reverse('home'))
        messages_list = list(response_message.context['messages'])
        self.assertEqual(len(messages_list), 2)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        after_count_user = User.objects.count()
        after_count_club_member = Club_Member.objects.count()
        after_count_club = Club.objects.count()
        self.assertEqual(after_count_user, before_count_user-1)
        self.assertEqual(after_count_club_member, before_count_club_member-1)
        self.assertEqual(after_count_club, before_count_club)
