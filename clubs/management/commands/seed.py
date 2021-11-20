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
        self.AUTHORIZATION_CHOICES = ['AP', 'ME', 'OF', 'OW']

    def handle(self, *args, **options):

        for i in range(0, 100):
            first_name=self.faker.first_name()
            last_name=self.faker.last_name()
            email = f'{first_name.lower()}{last_name.lower()}@example.org'
            bio=self.faker.sentence()
            personal_statement=self.faker.sentence()
            chess_experience= numpy.random.choice(self.CHESS_EXPERIENCE_CHOICES)
            password='Password123'
            randUser = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                bio=bio,
                personal_statement=personal_statement,
                chess_experience= chess_experience,
            )
            Club.objects.create(
                user=randUser,
                authorization=numpy.random.choice(self.AUTHORIZATION_CHOICES)
            )
