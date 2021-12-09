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

    def assert_main_narbar(self, response):
        for url in self.main_navbar_urls:
            with self.assertHTML(response, f'a[href="{url}"]'):
                pass

    def assert_no_main_navbar(self, response):
        for url in self.main_navbar_urls:
            self.assertNotHTML(response, f'a[href="{url}"]')

    def assert_club_navbar(self, response, club_id):
        club_navbar_urls = [
            reverse('show_club', kwargs={'club_id': club_id}),
            reverse('members_list', kwargs={'club_id': club_id}),
            # reverse('applicants_list', kwargs={'club_id': club_id}),
        ]
        for url in club_navbar_urls:
            with self.assertHTML(response, f'a[href="{url}"]'):
                pass

    def assert_no_club_navbar(self, response, club_id):
        club_navbar_urls = [
            reverse('show_club', kwargs={'club_id': club_id}),
            reverse('members_list', kwargs={'club_id': club_id}),
            # reverse('applicants_list', kwargs={'club_id': club_id}), Some user cannot see applicants_list so it is commented. Will remove in future if not needed
        ]
        for url in club_navbar_urls:
            self.assertNotHTML(response, f'a[href="{url}"]')
