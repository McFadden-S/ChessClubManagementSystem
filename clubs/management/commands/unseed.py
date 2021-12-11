from django.core.management.base import BaseCommand, CommandError
from clubs.models import User, Club_Member, Club

class Command(BaseCommand):
    """The database unseeder."""
    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            if not user.is_staff and not user.is_superuser:
                user.delete()

        clubs = Club.objects.all()
        for club in clubs:
            club.delete()

        club_members = Club_Member.objects.all()
        for club_member in club_members:
            club_member.delete()
