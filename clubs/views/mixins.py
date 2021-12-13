"""Mixins for the views."""
from clubs.helpers import get_authorization, get_club
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

class LoginProhibitedMixin():
    """Mixin that redirects when a user is logged in."""

    def dispatch(self, *args, **kwargs):
        """Redirect when user is logged in, or dispatch as normal otherwise."""

        if self.request.user.is_authenticated:
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        return super().dispatch(*args, **kwargs)

class ClubAuthorizationRequiredMixin(LoginRequiredMixin):
    """Mixin that redirects the user if the user does not have an authorization."""

    def dispatch(self, *args, **kwargs):
        """Redirect when user does not have an authorization, or dispatch as normal otherwise."""

        if get_authorization(self.request.user, get_club(self.kwargs['club_id'])) == None:
            messages.add_message(self.request, messages.ERROR, "You are not a part of this club")
            return redirect(settings.REDIRECT_URL_WHEN_NO_CLUB_AUTHORIZATION)
        return super().dispatch(*args, **kwargs)

class ApplicantsOnlyMixin(ClubAuthorizationRequiredMixin):
    """Mixin that redirects the user if the user is not applicant."""

    def dispatch(self, *args, **kwargs):
        """Redirect when user is not applicant, or dispatch as normal otherwise."""

        if get_authorization(self.request.user, get_club(self.kwargs['club_id'])) != 'AP':
            messages.add_message(self.request, messages.ERROR, "You are not an applicant")
            return redirect(settings.REDIRECT_URL_WHEN_MEMBER, self.kwargs['club_id'])
        return super().dispatch(*args, **kwargs)

class MembersRequiredMixin(ClubAuthorizationRequiredMixin):
    """Mixin that redirects the user if the user is applicant."""

    def dispatch(self, *args, **kwargs):
        """Redirect when user is applicant, or dispatch as normal otherwise."""

        if get_authorization(self.request.user, get_club(self.kwargs['club_id'])) == 'AP':
            messages.add_message(self.request, messages.ERROR, "You are not a member of this club")
            return redirect(settings.REDIRECT_URL_WHEN_APPLICANT, self.kwargs['club_id'])
        return super().dispatch(*args, **kwargs)

class OfficersRequiredMixin(MembersRequiredMixin):
    """Mixin that redirects the user if the user is member."""

    def dispatch(self, *args, **kwargs):
        """Redirect when user is member, or dispatch as normal otherwise."""

        if get_authorization(self.request.user, get_club(self.kwargs['club_id'])) == 'ME':
            messages.add_message(self.request, messages.ERROR, "You are not an officer of this club")
            return redirect(settings.REDIRECT_URL_WHEN_MEMBER, self.kwargs['club_id'])
        return super().dispatch(*args, **kwargs)

class OwnersRequiredMixin(OfficersRequiredMixin):
    """Mixin that redirects the user if the user is officer."""

    def dispatch(self, *args, **kwargs):
        """Redirect when user is officer, or dispatch as normal otherwise."""

        if get_authorization(self.request.user, get_club(self.kwargs['club_id'])) == 'OF':
            messages.add_message(self.request, messages.ERROR, "You are not the owner of this club")
            return redirect(settings.REDIRECT_URL_WHEN_OFFICER, self.kwargs['club_id'])
        return super().dispatch(*args, **kwargs)
