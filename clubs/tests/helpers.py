"""Helper methods for the unit tests"""
from django.urls import reverse
from with_asserts.mixin import AssertHTMLMixin

def reverse_with_next(url_name, next_url):
    url = reverse(url_name)
    url += f"?next={next_url}"
    return url

class LogInTester:
    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()

class NavbarTesterMixin(AssertHTMLMixin):
    main_navbar_urls = [
        reverse('update_user'), reverse('change_password'),
        reverse('delete_account'), reverse('log_out')
    ]

    def assert_main_navbar(self, response):
        for url in self.main_navbar_urls:
            with self.assertHTML(response, f'a[href="{url}"]'):
                pass

        self.assertContains(response, "Chess")
        self.assertContains(response, "My Clubs")
        self.assertContains(response, "Change profile")
        self.assertContains(response, "Change password")
        self.assertContains(response, "Delete account")
        self.assertContains(response, "Log out")

    def assert_no_main_navbar(self, response):
        for url in self.main_navbar_urls:
            self.assertNotHTML(response, f'a[href="{url}"]')

        self.assertNotContains(response, "Chess")
        self.assertNotContains(response, "My Clubs")
        self.assertNotContains(response, "Change profile")
        self.assertNotContains(response, "Change password")
        self.assertNotContains(response, "Delete account")
        self.assertNotContains(response, "Log out")

    def assert_club_navbar(self, response, club_id):
        club_navbar_urls = [
            reverse('show_club', kwargs={'club_id': club_id}),
            reverse('members_list', kwargs={'club_id': club_id}),
        ]
        for url in club_navbar_urls:
            with self.assertHTML(response, f'a[href="{url}"]'):
                pass

        self.assertContains(response, "Club")
        self.assertContains(response, "Members")

    def assert_no_club_navbar(self, response, club_id):
        club_navbar_urls = [
            reverse('show_club', kwargs={'club_id': club_id}),
            reverse('members_list', kwargs={'club_id': club_id}),
        ]
        for url in club_navbar_urls:
            self.assertNotHTML(response, f'a[href="{url}"]')

        self.assertNotContains(response, "Club")
        self.assertNotContains(response, "Members")
