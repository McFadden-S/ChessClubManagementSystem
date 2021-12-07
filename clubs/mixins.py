from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.conf import settings
from .helpers import get_authorization, get_club
from django.contrib import messages

class LoginProhibitedMixin():

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        return super().dispatch(*args, **kwargs)

class ClubAuthorizationRequiredMixin(LoginRequiredMixin):

    def dispatch(self, *args, **kwargs):
        if get_authorization(self.request.user, get_club(self.kwargs['club_id'])) == None:
            messages.add_message(self.request, messages.ERROR, "You are not a part of this club")
            return redirect(settings.REDIRECT_URL_WHEN_NO_CLUB_AUTHORIZATION)
        return super().dispatch(*args, **kwargs)

class ApplicantsOnlyMixin(ClubAuthorizationRequiredMixin):

    def dispatch(self, *args, **kwargs):
        if get_authorization(self.request.user, get_club(self.kwargs['club_id'])) != 'AP':
            messages.add_message(self.request, messages.ERROR, "You are not an applicant")
            return redirect(settings.REDIRECT_URL_WHEN_MEMBER, self.kwargs['club_id'])
        return super().dispatch(*args, **kwargs)

class MembersRequiredMixin(ClubAuthorizationRequiredMixin):

    def dispatch(self, *args, **kwargs):
        if get_authorization(self.request.user, get_club(self.kwargs['club_id'])) == 'AP':
            messages.add_message(self.request, messages.ERROR, "You are not a member of this club")
            return redirect(settings.REDIRECT_URL_WHEN_APPLICANT, self.kwargs['club_id'])
        return super().dispatch(*args, **kwargs)

class OfficersRequiredMixin(MembersRequiredMixin):

    def dispatch(self, *args, **kwargs):
        if get_authorization(self.request.user, get_club(self.kwargs['club_id'])) == 'ME':
            messages.add_message(self.request, messages.ERROR, "You are not an officer of this club")
            return redirect(settings.REDIRECT_URL_WHEN_MEMBER, self.kwargs['club_id'])
        return super().dispatch(*args, **kwargs)

class OwnersRequiredMixin(OfficersRequiredMixin):

    def dispatch(self, *args, **kwargs):
        if get_authorization(self.request.user, get_club(self.kwargs['club_id'])) == 'OF':
            messages.add_message(self.request, messages.ERROR, "You are not the owner of this club")
            return redirect(settings.REDIRECT_URL_WHEN_OFFICER, self.kwargs['club_id'])
        return super().dispatch(*args, **kwargs)
