import math
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect,render
from django.urls import reverse
from django.conf import settings

from django.views.generic.edit import FormView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.views import View

from .forms import *
from .models import *
from .helpers import *
from .decorators import *
from .mixins import *


class HomeView(LoginProhibitedMixin, TemplateView):
    template_name = 'home.html'

class SignUpView(LoginProhibitedMixin, FormView):
    """View that signs up user."""

    form_class = SignUpForm
    template_name = "sign_up.html"

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        messages.success(self.request, f"Your account was created successfully")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('dashboard')

class LogInView(LoginProhibitedMixin, FormView):
    """View to log in to the system."""

    template_name = "log_in.html"
    form_class = LogInForm

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)

        if user is None:
            return super().form_invalid(form)

        login(self.request, user)
        messages.success(self.request, "Login Successful")
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('dashboard')

class UpdateUserView(LoginRequiredMixin, UpdateView):
    """View to update logged-in user's profile."""

    model = UserUpdateForm
    template_name = "user_update.html"
    form_class = UserUpdateForm

    def get_object(self):
        """Return the object (user) to be updated."""
        user = self.request.user
        return user

    def get_success_url(self):
        """Return redirect URL after successful update."""
        messages.success(self.request, "User Information Updated Successfully")
        return reverse('dashboard')

class ChangePasswordView(LoginRequiredMixin, FormView):
    """View to change logged-in user's password."""

    template_name = "change_password.html"
    form_class = UserChangePasswordForm

    def form_valid(self, form):
        current_user = self.request.user
        password = form.cleaned_data.get('password')

        if check_password(password, current_user.password):
            new_password = form.cleaned_data.get('new_password')
            current_user.set_password(new_password)
            current_user.save()
            login(self.request, current_user)

            messages.success(self.request, "Password Changed Successfully")
            return super().form_valid(form)

        else:
            return super().form_invalid(form)

    def get_success_url(self):
        return reverse('dashboard')

class CreateClubView(LoginRequiredMixin, FormView):
    template_name = "create_club.html"
    form_class = CreateClubForm

    def form_valid(self,form):
        current_user = self.request.user
        try:
            club_created = form.save()
            Club_Member.objects.create(user=current_user, club=club_created, authorization='OW')
            messages.success(self.request, "Club created Successfully")
            return super().form_valid(form)
        except IndexError:
            messages.error(self.request, "Invalid address")
            form_new = CreateClubForm()
            return render(self.request,'create_club.html',{'form': form_new})

    def get_success_url(self):
        return reverse('dashboard')

class WaitingListView(ApplicantsOnlyMixin, TemplateView):
    """ View for the waiting list for applicants to a club """

    template_name = 'waiting_list.html'

@login_required
def log_out(request):
    logout(request)
    return redirect('home')

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

    return render(request, 'members_list.html', {'club_id': kwargs['club_id'], 'members': members, 'officers': officers, 'owners': owners})

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

    return render(request, 'applicants_list.html', {'club_id' : kwargs['club_id'], 'applicants': applicants})

class ShowView(TemplateView):

    def get(self, request, *args, **kwargs):
        club = get_club(kwargs['club_id'])
        user = get_user(kwargs[self.id_name])

        if user == None or self.is_show_authorization_correct(user, club):
            return redirect(self.redirect_location, kwargs['club_id'])

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        club = get_club(kwargs['club_id'])
        user = get_user(kwargs[self.id_name])

        context['club_id'] = kwargs['club_id']
        context['user'] = user
        context['authorizationText'] = get_authorization_text(user, club)
        context['request_from_owner'] = is_owner(self.request.user, club)
        context['request_from_officer'] = is_officer(self.request.user, club)

        return context

class ShowMemberView(MembersRequiredMixin, ShowView):

    template_name = 'show_member.html'
    redirect_location = 'members_list'
    id_name = 'member_id'

    def is_show_authorization_correct(self, user, club):
        return get_authorization_text(user, club) == None

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class ShowApplicantView(OfficersRequiredMixin, ShowView):

    template_name = 'show_applicant.html'
    redirect_location = 'applicants_list'
    id_name = 'applicant_id'

    def is_show_authorization_correct(self, user, club):
        return not is_applicant(user, club)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

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

@login_required
def apply_club(request, *args, **kwargs):
    current_user = request.user
    club = get_club(kwargs['club_id'])
    if not is_user_in_club(current_user, club):
        Club_Member.objects.create(user=current_user, club=club, authorization='AP')
        return render(request,'waiting_list.html', {'club_id' : kwargs['club_id']})
    return redirect('dashboard')

@login_required
def delete_account(request):
    my_clubs = get_my_clubs(request.user)
    remove_clubs(request.user, my_clubs)

    # Delete the user from club_member and user table
    request.user.delete()
    messages.add_message(request, messages.SUCCESS, "Your account has been deleted")
    return redirect('home')

@login_required
def dashboard(request, *args, **kwargs):
    current_user = request.user
    my_clubs = get_my_clubs(current_user)
    other_clubs = get_other_clubs(current_user)

    if 'search_btn' in request.POST:
        if request.method == 'POST':
            searched_letters = request.POST['searched_letters']
            if searched_letters:
                my_clubs = get_clubs_search(searched_letters)
                other_clubs = get_clubs_search(searched_letters)

    if 'sort_table' in request.POST:
        if request.method == 'POST':
            sort_table = request.POST['sort_table']
            my_clubs = my_clubs.order_by(sort_table)
            other_clubs = other_clubs.order_by(sort_table)

    club_auth = get_club_to_auth(current_user, my_clubs)
    return render(request,'dashboard.html', {'other_clubs': other_clubs, 'my_clubs': my_clubs, 'club_auth': club_auth})

@login_required
def show_club(request, *args, **kwargs):
    club = get_club(kwargs['club_id'])

    if club == None:
        return redirect('dashboard')

    owner = get_owners(club).first()

    return render(request, 'show_club.html', {'club_id': kwargs['club_id'], 'club': club, 'owner': owner, 'is_user_in_club': is_user_in_club(request.user, club)})
