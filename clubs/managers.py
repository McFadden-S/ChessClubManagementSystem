from django.contrib.auth.base_user import BaseUserManager
import clubs.models

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **other_fields):

        if email is None:
            raise TypeError('Users must have an email address.')

        email = self.normalize_email(email)
        user = self.model(email = email, **other_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if other_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        user = self.create_user(email, password, **other_fields)
        clubs.models.Club_Member.objects.create(user=user, authorization='OW')
        return user
