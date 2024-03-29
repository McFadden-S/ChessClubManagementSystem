"""Views for showing-detail-related purposes."""
from clubs.helpers import *
from clubs.views.mixins import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class ShowView(TemplateView):
    """Abstract Class for Views that show an object in the application."""

    def get(self, request, *args, **kwargs):
        """Handle get request and redirect user to appropriate page if show view is not possible."""

        if not self.is_show_correct(**kwargs):
            return self.incorrect_show_redirect(**kwargs)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Generate context data to be shown in the template."""

        context = super().get_context_data(**kwargs)
        club = get_club(kwargs['club_id'])
        current_user = self.request.user

        context['club_id'] = kwargs['club_id']
        context['my_clubs'] = get_my_clubs(current_user)
        context['my_authorization'] = get_authorization_text(current_user, club)

        return context

class ShowClubView(LoginRequiredMixin, ShowView):
    """View Class to handle the display of a club."""

    template_name = "show_club.html"

    def is_show_correct(self, **kwargs):
        """Check if the club exist."""

        club = get_club(kwargs['club_id'])
        return club != None

    def incorrect_show_redirect(self, **kwargs):
        """Redirect the user to dashboard if the club that needs to be shown does not exist."""

        return redirect('dashboard')

    def get_context_data(self, **kwargs):
        """Generate context data to be shown in the template."""

        context = super().get_context_data(**kwargs)
        club = get_club(kwargs['club_id'])
        owner = get_owners(club).first()
        current_user = self.request.user

        context['club'] = club
        context['owner'] = owner
        context['is_user_in_club'] = is_user_in_club(current_user, club)

        return context

class ShowClubUserView(ShowView):
    """Abstract Class for Views that show an user in a club in the application."""

    def incorrect_show_redirect(self, **kwargs):
        """Redirect user to appropriate page if showing the club user is not possible."""

        return redirect(self.redirect_location, kwargs['club_id'])

    def is_show_correct(self, **kwargs):
        """Check if the user exist and if the user is in the given club."""

        club = get_club(kwargs['club_id'])
        user = get_user(kwargs[self.id_name])
        return user != None and self.is_show_user_correct(user, club)

    def get_context_data(self, **kwargs):
        """Generate context data to be shown in the template."""

        context = super().get_context_data(**kwargs)
        context['user'] = get_user(kwargs[self.id_name])

        return context

class ShowMemberView(MembersRequiredMixin, ShowClubUserView):
    """View Class for showing a Member/Officer/Owner of a club."""

    template_name = 'show_member.html'
    redirect_location = 'members_list'
    id_name = 'member_id'

    def is_show_user_correct(self, user, club):
        """Check if there is an authorization for the user in the given club."""

        return  get_authorization_text(user, club) != None

    def get(self, request, *args, **kwargs):
        """Handle get request."""

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Generate context data to be shown in the template."""

        context = super().get_context_data(**kwargs)
        club = get_club(kwargs['club_id'])
        user = get_user(kwargs[self.id_name])
        context['authorizationText'] = get_authorization_text(user, club)
        context['chess_experience'] = get_chess_experience_text(user)

        return context

class ShowApplicantView(OfficersRequiredMixin, ShowClubUserView):
    """View Class for showing an applicant of a club."""

    template_name = 'show_applicant.html'
    redirect_location = 'applicants_list'
    id_name = 'applicant_id'

    def is_show_user_correct(self, user, club):
        """Check if the user is an applicant in the given club."""

        return is_applicant(user, club)

    def get(self, request, *args, **kwargs):
        """Handle get request."""

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Generate context data to be shown in the template."""

        context = super().get_context_data(**kwargs)
        user = get_user(kwargs[self.id_name])
        context['chess_experience'] = get_chess_experience_text(user)
        return context
