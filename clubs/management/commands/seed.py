from django.core.management.base import BaseCommand, CommandError
from faker import Faker
import numpy
from clubs.models import User, Club

class Command(BaseCommand):
    """The database seeder."""
    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')
        self.CHESS_EXPERIENCE_CHOICES = ['Beginner', 'Intermediate', 'Advanced']
        self.AUTHORIZATION_CHOICES = ['Applicant', 'Member', 'Officer', 'Owner']

    def handle(self, *args, **options):

        for i in range(0, 100):
            randUser = User.objects.create_user(
                first_name=self.faker.first_name(),
                last_name=self.faker.last_name(),
                email=self.faker.email(),
                bio=self.faker.sentence(),
                personal_statement=self.faker.sentence(),
                chess_experience= numpy.random.choice(self.CHESS_EXPERIENCE_CHOICES),
                password=self.faker.password(),
            )
            Club.objects.create(
                user=randUser,
                authorization=numpy.random.choice(self.AUTHORIZATION_CHOICES)
            )
