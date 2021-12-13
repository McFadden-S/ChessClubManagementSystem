from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from clubs.helpers import *
from .mixins import *

class ActionView(TemplateView):
    """Abstract Class for Views that make an action in the application."""

    def get(self, request, *args, **kwargs):
        """Handle get request."""

        club = get_club(kwargs['club_id'])
        current_user = request.user
        user = get_user(kwargs[self.id_name])
        if (self.is_actionable(current_user, user, club)):
            self.action(current_user, user, club)
        return redirect(self.redirect_location, kwargs['club_id'])

class ApproveApplicantView(OfficersRequiredMixin, ActionView):
    """View to approve applicant and change authorization to member"""

    redirect_location = 'applicants_list'
    id_name = 'applicant_id'

    def is_actionable(self, current_user, user, club):
        """Check if the user can be promoted."""

        return (is_officer(current_user, club) or is_owner(current_user, club)) and is_applicant(user, club)

    def action(self, current_user, user, club):
        """Change user's authorization from applicant to member"""

        set_authorization(user, club, "ME")

    def get(self, request, *args, **kwargs):
        """Handle get request."""

        return super().get(request, *args, **kwargs)

class RejectApplicantView(OfficersRequiredMixin, ActionView):
    """View to reject the applicant and remove the applicant from the club."""

    redirect_location = 'applicants_list'
    id_name = 'applicant_id'

    def is_actionable(self, current_user, user, club):
        """Check if the applicant can be rejected."""

        return (is_officer(current_user, club) or is_owner(current_user, club)) and is_applicant(user, club)

    def action(self, current_user, user, club):
        """Remove the applicant from the club."""

        remove_user_from_club(user, club)

    def get(self, request, *args, **kwargs):
        """Handle get request."""

        return super().get(request, *args, **kwargs)

class PromoteMemberView(OwnersRequiredMixin, ActionView):
    """View to promote the member to officer."""

    redirect_location = 'members_list'
    id_name = 'member_id'

    def is_actionable(self, current_user, user, club):
        """Check if the member can be promoted."""

        return is_owner(current_user, club) and is_member(user, club)

    def action(self, current_user, user, club):
        """Promote member to officer."""

        set_authorization(user, club, "OF")

    def get(self, request, *args, **kwargs):
        """Handle get request."""

        return super().get(request, *args, **kwargs)

class DemoteOfficerView(OwnersRequiredMixin, ActionView):
    """View to demote officer to member."""

    redirect_location = 'members_list'
    id_name = 'member_id'

    def is_actionable(self, current_user, user, club):
        """Check if officer can be demoted."""

        return is_owner(current_user, club) and is_officer(user, club)

    def action(self, current_user, user, club):
        """Demote the officer to member"""

        set_authorization(user, club, "ME")

    def get(self, request, *args, **kwargs):
        """Handle get request."""

        return super().get(request, *args, **kwargs)

class RemoveUserView(OfficersRequiredMixin, ActionView):
    """View to remove the user from the club"""

    redirect_location = 'members_list'
    id_name = 'user_id'

    def is_actionable(self, current_user, user, club):
        """Check if the user can be removed."""

        cu_is_owner = is_owner(current_user, club)
        cu_is_officer = is_officer(current_user, club)
        u_is_officer = is_officer(user, club)
        u_is_member = is_member(user, club)
        return (cu_is_owner and (u_is_officer or u_is_member)) or (cu_is_officer and u_is_member)

    def action(self, current_user, user, club):
        """Remove user from the club"""

        remove_user_from_club(user, club)

    def get(self, request, *args, **kwargs):
        """Handle get request."""

        return super().get(request, *args, **kwargs)

class TransferOwnershipView(OwnersRequiredMixin, ActionView):
    """View to transfer ownership to another officer"""

    redirect_location = 'members_list'
    id_name = 'member_id'

    def is_actionable(self, current_user, user, club):
        """Check if the ownership can be transferred to a valid officer."""

        return is_owner(current_user, club) and is_officer(user, club)

    def action(self, current_user, user, club):
        """Transfer ownership to officer and demote owner to officer."""

        set_authorization(user, club, "OW")
        set_authorization(current_user, club, "OF")

    def get(self, request, *args, **kwargs):
        """Handle get request."""

        return super().get(request, *args, **kwargs)

class LeaveClubView(LoginRequiredMixin, ActionView):
    """View that lets the user leave a club."""

    redirect_location = 'dashboard'

    def is_actionable(self, current_user, club):
        """Check if the user can leave the club."""
        # Only members and officers can leave a club
        return is_member(current_user, club) or is_officer(current_user, club)

    def action(self, current_user, club):
        """Remove the user from the club."""

        remove_user_from_club(current_user, club)

    def get(self, request, *args, **kwargs):
        """Handle get request and redirect the user to dashboard if the user is not able to leave the club."""

        club = get_club(kwargs['club_id'])
        current_user = request.user
        if (self.is_actionable(current_user, club)):
            self.action(current_user, club)
        return redirect(self.redirect_location)

#Mainined ActionView REVIEW IF CAN BE AN ActionView
class ApplyClubView(LoginRequiredMixin, TemplateView):
    """View that allows user to apply for a club."""

    redirect_location = 'dashboard'

    def is_actionable(self, current_user, user, club):
        """Check if the user is in the club that the user is trying to apply to."""

        return not is_user_in_club(current_user, club)

    def action(self, current_user, user, club):
        """Set the user's authorization to an applicant for the club and redirect to waiting list."""

        Club_Member.objects.create(user=current_user, club=club, authorization='AP')
        self.redirect_location = 'waiting_list'

    def get(self, request, *args, **kwargs):
        """Handle get request and redirect user to dashboard if user is not able to apply for the club."""

        club = get_club(kwargs['club_id'])
        current_user = request.user
        user = None

        if (self.is_actionable(current_user, user, club)):
            self.action(current_user, user, club)
            return redirect(self.redirect_location, kwargs['club_id'])
        return redirect(self.redirect_location)

class DeleteAccountView(LoginRequiredMixin, TemplateView):
    """View to allow user to delete their account."""

    redirect_location = 'members_list'

    def is_actionable(self, current_user):
        """Check if the user's account can be deleted."""

        my_clubs = get_my_clubs(current_user)
        return remove_clubs(current_user, my_clubs)[0] == False

    def alternative_action(self, request, current_user):
        """Delete the user's account and redirect the user to home page."""

        current_user.delete()
        messages.add_message(request, messages.SUCCESS, "Your account has been deleted")
        self.redirect_location = 'home'

    def action(self, request, current_user):
        """Show a message that the user must transfer an ownership to someone in order to delete their account."""

        my_clubs = get_my_clubs(current_user)
        messages.add_message(request, messages.ERROR, "You must transfer ownership to a new owner")
        return remove_clubs(current_user, my_clubs)[1]

    def get(self, request, *args, **kwargs):
        """Handle get request."""

        current_user = request.user

        if (self.is_actionable(current_user)):
            return redirect(self.redirect_location, self.action(request, current_user))
        self.alternative_action(request, current_user)
        return redirect(self.redirect_location)
