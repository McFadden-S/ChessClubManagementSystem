"""Models in the clubs app."""
from clubs.managers import UserManager
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.db import models
from libgravatar import Gravatar

class User(AbstractUser):
    """User model for authentication."""

    username = None
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank = False)
    bio = models.CharField(max_length=720, blank=True)

    BEGINNER = 'BG'
    INTERMEDIATE = 'IM'
    ADVANCED = 'AV'
    CHESS_EXPERIENCE_CHOICES = [
        (BEGINNER, 'Beginner'),
        (INTERMEDIATE, 'Intermediate'),
        (ADVANCED, 'Advanced'),
    ]
    chess_experience = models.CharField(
        max_length=2,
        choices=CHESS_EXPERIENCE_CHOICES,
        default=BEGINNER
    )

    personal_statement = models.CharField(max_length=720, blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    def gravatar(self, size=100):
        """Return a URL to the user's gravatar."""

        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to a smaller version of user's gravatar."""

        return self.gravatar(size=60)

class Club(models.Model):
    """Clubs created by users in chess club management system."""

    name = models.CharField(max_length=50, unique=True, blank=False)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    country = CountryField(blank_label='(select country)')
    description = models.CharField(max_length=500, blank=False)

class Club_Member(models.Model):
    """Authorization for each member in a club."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, blank=False)

    APPLICANT = 'AP'
    MEMBER = 'ME'
    OFFICER = 'OF'
    OWNER = 'OW'
    AUTHORIZATION_CHOICES = [
        (APPLICANT, 'Applicant'),
        (MEMBER, 'Member'),
        (OFFICER, 'Officer'),
        (OWNER, 'Owner')
    ]

    authorization = models.CharField(
        max_length=2,
        choices=AUTHORIZATION_CHOICES,
        default=APPLICANT
    )

    class Meta:
        """Model options."""

        unique_together = (("user", "club"),)
