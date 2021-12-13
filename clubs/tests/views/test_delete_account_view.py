"""Tests of the delete account view."""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club_Member, Club
from clubs.tests.helpers import LogInTester
from django.contrib import messages
from clubs.tests.helpers import reverse_with_next

class DeleteAccountViewTestCase(TestCase, LogInTester):
    """Tests of the delete account view."""
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

    """ 1) Tests delete account url """
    def test_delete_account_url(self):
        self.assertEqual(self.url,'/delete_account/')

    """ 2) Tests for redirect when logged in """
    def test_get_delete_account_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertFalse(self._is_logged_in())

    """ 3) Tests delete account for single user in club """
    def test_any_user_without_club_can_delete_account(self):
        self.client.login(email=self.user.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count_user = User.objects.count()
        response = self.client.get(self.url)
        response2 = self.client.get(reverse('home'))
        messages_list = list(response2.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        after_count_user = User.objects.count()
        self.assertEqual(after_count_user, before_count_user-1)
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)

    """ 3.1) Tests delete account for applicant in club """
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
        response2 = self.client.get(reverse('home'))
        messages_list = list(response2.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        after_count_user = User.objects.count()
        after_count_club_member = Club_Member.objects.count()
        after_count_club = Club.objects.count()
        self.assertEqual(after_count_user, before_count_user-1)
        self.assertEqual(after_count_club_member, before_count_club_member-1)
        #club still exists because owner still present
        self.assertEqual(after_count_club, before_count_club)
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)


    """ 3.2) Tests delete account for member in club """
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
        response2 = self.client.get(reverse('home'))
        messages_list = list(response2.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        after_count_user = User.objects.count()
        after_count_club_member = Club_Member.objects.count()
        after_count_club = Club.objects.count()
        self.assertEqual(after_count_user, before_count_user-1)
        self.assertEqual(after_count_club_member, before_count_club_member-1)
        #club still exists because owner still present
        self.assertEqual(after_count_club, before_count_club)
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)

    """ 3.3) Tests delete account for officer in club """
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
        response2 = self.client.get(reverse('home'))
        messages_list = list(response2.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        after_count_user = User.objects.count()
        after_count_club_member = Club_Member.objects.count()
        after_count_club = Club.objects.count()
        self.assertEqual(after_count_user, before_count_user-1)
        self.assertEqual(after_count_club_member, before_count_club_member-1)
        #club still exists because owner still present
        self.assertEqual(after_count_club, before_count_club)
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)

    """ 3.4) Tests delete account for owner in club """
    def test_owner_who_is_only_person_in_club_can_delete_account(self):
        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count_user = User.objects.count()
        before_count_club_member = Club_Member.objects.count()
        before_count_club = Club.objects.count()
        response = self.client.get(self.url)
        response2 = self.client.get(reverse('home'))
        messages_list = list(response2.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        after_count_user = User.objects.count()
        after_count_club_member = Club_Member.objects.count()
        after_count_club = Club.objects.count()
        self.assertEqual(after_count_user, before_count_user-1)
        self.assertEqual(after_count_club_member, before_count_club_member-1)
        self.assertEqual(after_count_club, before_count_club-1)
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)


    """4) Tests owner with single user of another type in club"""
    def test_owner_who_only_has_applicants_in_club_can_delete_account(self):
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
        response2 = self.client.get(reverse('home'))
        messages_list = list(response2.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        after_count_user = User.objects.count()
        after_count_club_member = Club_Member.objects.count()
        after_count_club = Club.objects.count()
        self.assertEqual(after_count_user, before_count_user-1)
        self.assertEqual(after_count_club_member, before_count_club_member-2)
        self.assertEqual(after_count_club, before_count_club-1)
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)

    """4.1) Tests owner with single user of member in club"""
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
        response2 = self.client.get(reverse('members_list', kwargs={'club_id' : self.club.id}))
        messages_list = list(response2.context['messages'])
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
        response2 = self.client.get(reverse('home'))
        messages_list = list(response2.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        after_count_user = User.objects.count()
        after_count_club_member = Club_Member.objects.count()
        after_count_club = Club.objects.count()
        self.assertEqual(after_count_user, before_count_user-1)
        self.assertEqual(after_count_club_member, before_count_club_member-1)
        self.assertEqual(after_count_club, before_count_club)

    """4.2) Tests owner with single user of officer in club"""
    def test_owner_who_has_only_has_officer_in_club_must_transfer_ownership(self):
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
        response2 = self.client.get(reverse('members_list', kwargs={'club_id' : self.club.id}))
        messages_list = list(response2.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)
        self.assertRedirects(response, reverse('members_list', kwargs={'club_id' : self.club.id}), status_code=302, target_status_code=200)
        #Owner transfers ownership from officer to owner
        url_transfer = reverse('transfer_ownership', kwargs={'club_id': self.club.id, 'member_id': club_officer.id})
        self.client.get(url_transfer)
        #Original owner now deletes account
        self.client.get(self.url)
        response2 = self.client.get(reverse('home'))
        messages_list = list(response2.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        after_count_user = User.objects.count()
        after_count_club_member = Club_Member.objects.count()
        after_count_club = Club.objects.count()
        self.assertEqual(after_count_user, before_count_user-1)
        self.assertEqual(after_count_club_member, before_count_club_member-1)
        self.assertEqual(after_count_club, before_count_club)


    """4.3) Tests for owner who has applicant and officer users"""
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
        response2 = self.client.get(reverse('members_list', kwargs={'club_id' : self.club.id}))
        messages_list = list(response2.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)
        self.assertRedirects(response, reverse('members_list', kwargs={'club_id' : self.club.id}), status_code=302, target_status_code=200)
        #Owner transfers ownership from officer to owner
        url_transfer = reverse('transfer_ownership', kwargs={'club_id': self.club.id, 'member_id': User.objects.get(email='bethsmith@example.org').id})
        self.client.get(url_transfer)
        #Original owner now deletes account
        self.client.get(self.url)
        response2 = self.client.get(reverse('home'))
        messages_list = list(response2.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        after_count_user = User.objects.count()
        after_count_club_member = Club_Member.objects.count()
        after_count_club = Club.objects.count()
        self.assertEqual(after_count_user, before_count_user-1)
        self.assertEqual(after_count_club_member, before_count_club_member-1)
        self.assertEqual(after_count_club, before_count_club)

    """4.4) Tests for owner who has applicant and member as users"""
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
        response2 = self.client.get(reverse('members_list', kwargs={'club_id' : self.club.id}))
        messages_list = list(response2.context['messages'])
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
        response2 = self.client.get(reverse('home'))
        messages_list = list(response2.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        after_count_user = User.objects.count()
        after_count_club_member = Club_Member.objects.count()
        after_count_club = Club.objects.count()
        self.assertEqual(after_count_user, before_count_user-1)
        self.assertEqual(after_count_club_member, before_count_club_member-1)
        self.assertEqual(after_count_club, before_count_club)

    """4.5) Tests for owner who has officer and member as users"""
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
        response2 = self.client.get(reverse('members_list', kwargs={'club_id' : self.club.id}))
        messages_list = list(response2.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)
        self.assertRedirects(response, reverse('members_list', kwargs={'club_id' : self.club.id}), status_code=302, target_status_code=200)
        #Owner transfers ownership from officer to owner
        url_transfer = reverse('transfer_ownership', kwargs={'club_id': self.club.id, 'member_id': User.objects.get(email='bethsmith@example.org').id})
        self.client.get(url_transfer)
        #Original owner now deletes account
        self.client.get(self.url)
        response2 = self.client.get(reverse('home'))
        messages_list = list(response2.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        after_count_user = User.objects.count()
        after_count_club_member = Club_Member.objects.count()
        after_count_club = Club.objects.count()
        self.assertEqual(after_count_user, before_count_user-1)
        self.assertEqual(after_count_club_member, before_count_club_member-1)
        self.assertEqual(after_count_club, before_count_club)
