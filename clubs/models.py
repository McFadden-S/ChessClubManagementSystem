from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from .managers import UserManager
from libgravatar import Gravatar

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
