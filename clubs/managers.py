"""Managers for models."""
import clubs.models
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    """Manager for the user model."""

    def create_user(self, email, password=None, **other_fields):
        """Create a new user."""

        if email is None:
            raise TypeError('Users must have an email address.')

        email = self.normalize_email(email)
        user = self.model(email = email, **other_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **other_fields):
        """Create a superuser."""

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self.create_user(email, password, **other_fields)
        club = clubs.models.Club.objects.create(name=f'{user.first_name.lower()}{user.last_name.lower()}', description="Admin Club")
        clubs.models.Club_Member.objects.create(user=user, club=club, authorization="OW")

        return user
