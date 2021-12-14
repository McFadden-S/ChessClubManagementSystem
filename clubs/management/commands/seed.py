"""The database seeder."""
from clubs.models import Club, Club_Member, User
from django.core.management.base import BaseCommand
from faker import Faker
import numpy

class Command(BaseCommand):
    """The database seeder."""
    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB', 0)
        self.CHESS_EXPERIENCE_CHOICES = ['Beginner', 'Intermediate', 'Advanced']
        self.AUTHORIZATION_CHOICES = ['AP', 'ME', 'OF']
        self.counter = 0

    def seed_random_user(self):
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

    def seed_random_club(self):
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

    def seed_test_users(self):

        jeb = User.objects.create_user(
            first_name='Jebediah',
            last_name='Kerman',
            email='jeb@example.org',
            bio='I am Test User 1',
            personal_statement='I Like Chess',
            chess_experience= 'BG',
            password = 'Password123',
        )

        val = User.objects.create_user(
            first_name='Valentina',
            last_name='Kerman',
            email='val@example.org',
            bio='I am Test User 2',
            personal_statement='I Like Chess',
            chess_experience= 'BG',
            password = 'Password123',
        )

        bil = User.objects.create_user(
            first_name='Billie',
            last_name='Kerman',
            email='billie@example.org',
            bio='I am Test User 3',
            personal_statement='I Like Chess',
            chess_experience= 'BG',
            password = 'Password123',
        )

        return [jeb, val, bil]

    def handle(self, *args, **options):
        test_users = self.seed_test_users()

        for i in range(0, 5):
            owner = self.seed_random_user()
            newClub = self.seed_random_club()

            # if structure to ensure data is set up to non-functional requirement
            if(i == 0):
                Club.objects.filter(id=newClub.id).update(name='Kerbal Chess Club')
                Club_Member.objects.create(
                    user=test_users[0],
                    club=newClub,
                    authorization='ME',
                )
                Club_Member.objects.create(
                    user=test_users[1],
                    club=newClub,
                    authorization='ME',
                )
                Club_Member.objects.create(
                    user=test_users[2],
                    club=newClub,
                    authorization='ME',
                )
            elif(i==1):
                Club_Member.objects.create(
                    user=test_users[0],
                    club=newClub,
                    authorization='OF',
                )
            elif(i==2):
                owner = test_users[1]
            elif(i==3):
                Club_Member.objects.create(
                    user=test_users[2],
                    club=newClub,
                    authorization='ME',
                )


            Club_Member.objects.create(
                user=owner,
                club=newClub,
                authorization='OW',
            )

            for j in range(0, 20):
                randUser = self.seed_random_user()
                Club_Member.objects.create(
                    user=randUser,
                    club=newClub,
                    authorization=numpy.random.choice(self.AUTHORIZATION_CHOICES)
                )
