from django.shortcuts import redirect,render
from django.views.generic import TemplateView
from django.contrib import messages

from clubs.helpers import *
from .mixins import *

class MembersListView(MembersRequiredMixin, TemplateView):

    template_name = "members_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        club = get_club(kwargs['club_id'])
        current_user = self.request.user

        context['club_id'] = kwargs['club_id']
        context['my_clubs'] = get_my_clubs(current_user)
        context['my_authorization'] = get_authorization_text(current_user, club)
        context['members'] = get_members(club)
        context['officers'] = get_officers(club)
        context['owners'] = get_owners(club)

        return context

class ApplicantsListView(OfficersRequiredMixin, TemplateView):

    template_name = "applicants_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        club = get_club(kwargs['club_id'])
        current_user = self.request.user

        context['club_id'] = kwargs['club_id']
        context['my_clubs'] = get_my_clubs(current_user)
        context['my_authorization'] = get_authorization_text(current_user, club)
        context['applicants'] = get_applicants(club)

        return context
