from django.core.management.base import BaseCommand, CommandError
from clubs.models import User, Club

class Command(BaseCommand):
    """The database unseeder."""
    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            if not user.is_staff and not user.is_superuser:
                user.delete()
