from django.core.management.base import BaseCommand, CommandError
from faker import Faker
import numpy
from clubs.models import User, Club_Member, Club

class Command(BaseCommand):
    """The database seeder."""
    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB', 0)
        self.CHESS_EXPERIENCE_CHOICES = ['Beginner', 'Intermediate', 'Advanced']
        self.AUTHORIZATION_CHOICES = ['AP', 'ME', 'OF']
        self.counter = 0

    def seedRandomUser(self):
        first_name=self.faker.first_name()
        last_name=self.faker.last_name()
        email = f'{first_name.lower()}{last_name.lower()}{self.counter}@example.org'
        bio=self.faker.sentence()
        personal_statement=self.faker.sentence()
        chess_experience= numpy.random.choice(self.CHESS_EXPERIENCE_CHOICES)

        randUser = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            bio=bio,
            personal_statement=personal_statement,
            chess_experience= chess_experience,
            password = 'Password123',
        )

        self.counter += 1
        return randUser

    def seedRandomClub(self):
        name = self.faker.text(max_nb_chars=20)
        address = self.faker.street_address()
        city = self.faker.city()
        postal_code = self.faker.postcode()
        country = self.faker.country_code()
        description = self.faker.sentence()

        newClub = Club.objects.create(
            name = name,
            address = address,
            city = city,
            postal_code = postal_code,
            country = country,
            description = description,
        )

        return newClub

    def handle(self, *args, **options):
        for i in range(0, 10):
            owner = self.seedRandomUser()
            newClub = self.seedRandomClub()

            Club_Member.objects.create(
                user=owner,
                club=newClub,
                authorization='OW',
            )

            for j in range(0, 50):
                randUser = self.seedRandomUser()
                Club_Member.objects.create(
                    user=randUser,
                    club=newClub,
                    authorization=numpy.random.choice(self.AUTHORIZATION_CHOICES)
                )
