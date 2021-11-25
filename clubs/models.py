from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from .managers import UserManager
from libgravatar import Gravatar
from location_field.models.plain import PlainLocationField
from django_countries.fields import CountryField

# Create your models here.
class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank = False)
    bio = models.CharField(max_length=100, blank=True)

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

    personal_statement = models.CharField(max_length=100, blank=True)

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

class Club_Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    club_name = models.CharField(max_length=50, default="club", blank=False)

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
        unique_together = (("user", "club_name"),)

class Club(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    country = CountryField(blank_label='(select country)')
    location = PlainLocationField(based_fields=['address', 'city', 'postal_code', 'country'], zoom=7, blank=True)
    description = models.CharField(max_length=500, blank=False)
