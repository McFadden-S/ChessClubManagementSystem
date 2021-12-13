"""Django-admin page contents registered here."""
from clubs.models import Club, Club_Member, User
from django.contrib import admin

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users."""

    list_display = [
        'email', 'first_name', 'last_name', 'chess_experience', 'is_active',
    ]

@admin.register(Club_Member)
class ClubMemberAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for club members."""

    list_display = [
        'user', 'club', 'authorization',
    ]

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for clubs."""

    list_display = [
        'name', 'address', 'city', 'postal_code', 'country',
    ]