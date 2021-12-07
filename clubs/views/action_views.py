from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from clubs.helpers import *
from .mixins import *

class ActionView(TemplateView):

    def get(self, request, *args, **kwargs):
        club = get_club(kwargs['club_id'])
        current_user = request.user
        user = get_user(kwargs[self.id_name])
        if (self.is_actionable(current_user, user, club)):
            self.action(current_user, user, club)
        return redirect(self.redirect_location, kwargs['club_id'])

class ApproveApplicantView(OfficersRequiredMixin, ActionView):

    redirect_location = 'applicants_list'
    id_name = 'applicant_id'

    def is_actionable(self, current_user, user, club):
        return (is_officer(current_user, club) or is_owner(current_user, club)) and is_applicant(user, club)

    def action(self, current_user, user, club):
        set_authorization(user, club, "ME")

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class RejectApplicantView(OfficersRequiredMixin, ActionView):
    """Reject the application and remove the applicant from the club."""

    redirect_location = 'applicants_list'
    id_name = 'applicant_id'

    def is_actionable(self, current_user, user, club):
        return (is_officer(current_user, club) or is_owner(current_user, club)) and is_applicant(user, club)

    def action(self, current_user, user, club):
        remove_user_from_club(user, club)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class PromoteMemberView(OwnersRequiredMixin, ActionView):

    redirect_location = 'members_list'
    id_name = 'member_id'

    def is_actionable(self, current_user, user, club):
        return is_owner(current_user, club) and is_member(user, club)

    def action(self, current_user, user, club):
        set_authorization(user, club, "OF")

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class DemoteOfficerView(OwnersRequiredMixin, ActionView):

    redirect_location = 'members_list'
    id_name = 'member_id'

    def is_actionable(self, current_user, user, club):
        return is_owner(current_user, club) and is_officer(user, club)

    def action(self, current_user, user, club):
        set_authorization(user, club, "ME")

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class RemoveUserView(OfficersRequiredMixin, ActionView):
    """Remove the user from the club"""

    redirect_location = 'members_list'
    id_name = 'user_id'

    def is_actionable(self, current_user, user, club):
        cu_is_owner = is_owner(current_user, club)
        cu_is_officer = is_officer(current_user, club)
        u_is_officer = is_officer(user, club)
        u_is_member = is_member(user, club)
        return (cu_is_owner and (u_is_officer or u_is_member)) or (cu_is_officer and u_is_member)

    def action(self, current_user, user, club):
        remove_user_from_club(user, club)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class TransferOwnershipView(OwnersRequiredMixin, ActionView):

    redirect_location = 'members_list'
    id_name = 'member_id'

    def is_actionable(self, current_user, user, club):
        return is_owner(current_user, club) and is_officer(user, club)

    def action(self, current_user, user, club):
        set_authorization(user, club, "OW")
        set_authorization(current_user, club, "OF")

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

#Mainined ActionView REVIEW IF CAN BE AN ActionView
class ApplyClubView(LoginRequiredMixin, TemplateView):

    redirect_location = 'dashboard'

    def is_actionable(self, current_user, user, club):
        return not is_user_in_club(current_user, club)

    def action(self, current_user, user, club):
        Club_Member.objects.create(user=current_user, club=club, authorization='AP')
        self.redirect_location = 'waiting_list'

    def get(self, request, *args, **kwargs):
        club = get_club(kwargs['club_id'])
        current_user = request.user
        user = None

        if (self.is_actionable(current_user, user, club)):
            self.action(current_user, user, club)
            return redirect(self.redirect_location, kwargs['club_id'])
        return redirect(self.redirect_location)
