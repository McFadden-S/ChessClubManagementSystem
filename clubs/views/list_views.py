from django.shortcuts import redirect,render
from django.views.generic import TemplateView
from django.contrib import messages

from clubs.helpers import *
from .mixins import *

from clubs.decorators import *
from django.contrib.auth.decorators import login_required

# To be implemented after javascript search sort complete
# class MembersListView(MembersRequiredMixin, TemplateView):
#
#     template_name = "members_list.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         club = get_club(kwargs['club_id'])
#
#         context['club_id'] = kwargs['club_id']
#         context['members'] = get_members(club)
#         context['officers'] = get_officers(club)
#         context['owners'] = get_owners(club)
#
#         return context

@login_required
@only_members
def members_list(request, *args, **kwargs):
    club = get_club(kwargs['club_id'])
    members = get_members(club)
    officers = get_officers(club)
    owners = get_owners(club)

    if 'search_btn' in request.POST:
        if request.method == 'POST':
            searched_letters = request.POST['searched_letters']
            if searched_letters:
                members = get_members_search(club, searched_letters)
                officers = get_officers_search(club, searched_letters)
                owners = get_owners_search(club, searched_letters)

    if 'sort_table' in request.POST:
        if request.method == 'POST':
            sort_table = request.POST['sort_table']
            members = members.order_by(sort_table)
            officers = officers.order_by(sort_table)
            owners = owners.order_by(sort_table)

    current_user = request.user
    my_clubs = get_my_clubs(current_user)
    my_authorization = get_authorization_text(current_user, club)
    return render(request, 'members_list.html', {'club_id': kwargs['club_id'], 'members': members, 'officers': officers, 'owners': owners, 'my_clubs': my_clubs, 'my_authorization': my_authorization})

# To be implemented after javascript search sort complete
# class ApplicantsListView(OfficersRequiredMixin, TemplateView):
#
#     template_name = "applicants_list.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         club = get_club(kwargs['club_id'])
#
#         context['club_id'] = kwargs['club_id']
#         context['applicants'] = get_applicants(club)
#
#         return context

@login_required
@only_officers
def applicants_list(request, *args, **kwargs):
    club = get_club(kwargs['club_id'])
    applicants = get_applicants(club)

    if 'search_btn' in request.POST:
        if request.method == 'POST':
            searched_letters = request.POST['searched_letters']
            if searched_letters:
                applicants = get_applicants_search(club, searched_letters)

    if 'sort_table' in request.POST:
        if request.method == 'POST':
            sort_table = request.POST['sort_table']
            applicants = applicants.order_by(sort_table)

    current_user = request.user
    my_clubs = get_my_clubs(current_user)
    my_authorization = get_authorization_text(current_user, club)
    return render(request, 'applicants_list.html', {'club_id' : kwargs['club_id'], 'applicants': applicants, 'my_clubs': my_clubs, 'my_authorization': my_authorization})
