from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from clubs.helpers import *
from .mixins import *


""" Abstract Class for Views that show an object in the application """
class ShowView(TemplateView):

    def get(self, request, *args, **kwargs):
        if not self.is_show_correct(**kwargs):
            return self.incorrect_show_redirect(**kwargs)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        club = get_club(kwargs['club_id'])
        current_user = self.request.user

        context['club_id'] = kwargs['club_id']
        context['my_clubs'] = get_my_clubs(current_user)
        context['my_authorization'] = get_authorization_text(current_user, club)

        return context

""" View Class to handle the display of a club """
class ShowClubView(LoginRequiredMixin, ShowView):

    template_name = "show_club.html"

    def is_show_correct(self, **kwargs):
        club = get_club(kwargs['club_id'])
        return club != None

    def incorrect_show_redirect(self, **kwargs):
        return redirect('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        club = get_club(kwargs['club_id'])
        owner = get_owners(club).first()
        current_user = self.request.user

        context['club'] = club
        context['owner'] = owner
        context['is_user_in_club'] = is_user_in_club(current_user, club)

        return context

""" Abstract Class for Views that show an user in a club in the application """
class ShowClubUserView(ShowView):

    def incorrect_show_redirect(self, **kwargs):
        return redirect(self.redirect_location, kwargs['club_id'])

    def is_show_correct(self, **kwargs):
        club = get_club(kwargs['club_id'])
        user = get_user(kwargs[self.id_name])
        return user != None and self.is_show_user_correct(user, club)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = get_user(kwargs[self.id_name])

        return context

""" View Class for showing a Member/Officer/Owner of a club"""
class ShowMemberView(MembersRequiredMixin, ShowClubUserView):

    template_name = 'show_member.html'
    redirect_location = 'members_list'
    id_name = 'member_id'

    def is_show_user_correct(self, user, club):
        return  get_authorization_text(user, club) != None

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        club = get_club(kwargs['club_id'])
        user = get_user(kwargs[self.id_name])
        context['authorizationText'] = get_authorization_text(user, club)

        return context

""" View Class for showing an applicant of a club"""
class ShowApplicantView(OfficersRequiredMixin, ShowClubUserView):

    template_name = 'show_applicant.html'
    redirect_location = 'applicants_list'
    id_name = 'applicant_id'

    def is_show_user_correct(self, user, club):
        return is_applicant(user, club)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
