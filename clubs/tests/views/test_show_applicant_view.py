from django.test import TestCase
from clubs.models import User,Club
from django.urls import reverse

class ShowApplicantViewTestCase(TestCase):
    def setUp(self):
        self.user =  User.objects.create_user(
            email='bobsmith@example.com',
            first_name = 'Bob',
            last_name = 'Smith',
            bio='Hi',
            chess_experience='AV',
            personal_statement = 'I am Orangutan',
            password="Orangutan123"
        )
        Club.objects.create(user=self.user)
        self.target_user = User.objects.get(email='bobsmith@example.com')
        self.url = reverse('show_applicant', kwargs={'applicant_id': self.target_user.id})

    def test_show_user_url(self):
        self.assertEqual(self.url, f'/show_applicant/{self.target_user.id}')

    def test_get_show_applicant(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_applicant.html')
        self.assertContains(response, "Bob Smith")
        self.assertContains(response, "Hi")
        self.assertContains(response, "AV")
        self.assertContains(response, "I am Orangutan")
