import math
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect,render
from django.urls import reverse
from django.conf import settings
from django.views.generic.edit import FormView, UpdateView
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

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

class WaitingListView(ApplicantsOnlyMixin, TemplateView):
    """ View for the waiting list for applicants to a club """

    template_name = 'waiting_list.html'

@login_required
def log_out(request):
    logout(request)
    return redirect('home')

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

@login_required
@only_members
def show_member(request, *args, **kwargs):
    club = get_club(kwargs['club_id'])
    member = get_user(kwargs['member_id'])
    authorizationText = get_authorization_text(member, club)

    if member == None or authorizationText == None:
        return redirect('members_list', kwargs['club_id'])

    return render(request, 'show_member.html',
        {'club_id': kwargs['club_id'],
        'member': member,
        'authorizationText' : authorizationText,
        'request_from_owner' : is_owner(request.user, club),
        'request_from_officer' : is_officer(request.user, club)})

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

@login_required
@only_officers
def show_applicant(request, *args, **kwargs):
    club = get_club(kwargs['club_id'])
    applicant = get_user(kwargs['applicant_id'])

    if applicant == None or not is_applicant(applicant, club):
        return redirect('applicants_list', kwargs['club_id'])

    return render(request, 'show_applicant.html',
        {'club_id' : kwargs['club_id'], 'applicant': applicant})

@login_required
@only_officers
def approve_applicant(request, *args, **kwargs):
    club = get_club(kwargs['club_id'])
    current_user = request.user
    applicant = get_user(kwargs['applicant_id'])
    if (is_officer(current_user, club) or is_owner(current_user, club)) and is_applicant(applicant, club):
        set_authorization(applicant, club, "ME")
        return redirect('applicants_list', kwargs['club_id'])
    return render(request, 'applicants_list.html', {'club_id' : kwargs['club_id'], 'applicants': applicants})

@login_required
@only_officers
def reject_applicant(request, *args, **kwargs):
    """Reject the application and remove the applicant from the club."""

    club = get_club(kwargs['club_id'])
    current_user = request.user
    applicant = get_user(kwargs['applicant_id'])
    if (is_officer(current_user, club) or is_owner(current_user, club)) and is_applicant(applicant, club):
        remove_user_from_club(applicant, club)
        return redirect('applicants_list', kwargs['club_id'])
    return render(request, 'applicants_list.html', {'club_id' : kwargs['club_id'], 'applicants': applicants})

@login_required
@only_owners
def promote_member(request, *args, **kwargs):
    club = get_club(kwargs['club_id'])
    current_user = request.user
    member = get_user(kwargs['member_id'])
    if is_owner(current_user, club) and is_member(member, club):
        set_authorization(member, club, "OF")
        return redirect(members_list, kwargs['club_id'])
    return render(request, 'members_list.html',
        {'club_id': kwargs['club_id'], 'member': member, 'auth' : get_authorization(current_user, club)})

@login_required
@only_owners
def demote_officer(request, *args, **kwargs):
    club = get_club(kwargs['club_id'])
    current_user = request.user
    member = get_user(kwargs['member_id'])
    if is_owner(current_user, club) and is_officer(member, club):
        set_authorization(member, club, "ME")
        return redirect(members_list, kwargs['club_id'])
    return render(request, 'members_list.html',
        {'club_id': kwargs['club_id'], 'member': member, 'auth' : get_authorization(current_user, club)})

@login_required
@only_officers
def remove_user(request, *args, **kwargs):
    """Remove the user from the club"""
    
    club = get_club(kwargs['club_id'])
    current_user = request.user
    user = get_user(kwargs['user_id'])
    if is_owner(current_user, club) and (is_officer(user, club) or is_member(user, club)):
        #Owner can remove both officers and members.
        remove_user_from_club(user, club)
        return redirect(members_list, kwargs['club_id'])
    elif is_officer(current_user, club) and is_member(user, club):
        #Officer can only remove members.
        remove_user_from_club(user, club)
        return redirect(members_list, kwargs['club_id'])
    return render(request, 'members_list.html',
        {'club_id': kwargs['club_id'], 'members': get_members(club), 'officers': get_officers(club), 'owners': get_owners(club)})

@login_required
@only_owners
def transfer_ownership(request, *args, **kwargs):
    club = get_club(kwargs['club_id'])
    current_user = request.user
    member = get_user(kwargs['member_id'])
    if is_owner(current_user, club) and is_officer(member, club):
        set_authorization(member, club, "OW")
        set_authorization(current_user, club, "OF")
        return redirect(members_list, kwargs['club_id'])
    return render(request, 'members_list.html',
        {'club_id': kwargs['club_id'], 'member': member, 'auth' : get_authorization(current_user, club)})

@login_required
def create_club(request, *args, **kwargs):
    if request.method == 'POST':
        current_user = request.user
        form = CreateClubForm(request.POST)
        if form.is_valid():
            try:
                club_created = form.save()
            except IndexError:
                messages.add_message(request, messages.ERROR, "The credentials provided were invalid")
                form_new = CreateClubForm()
                return render(request,'create_club.html',{'form': form_new})
            # redirect link needs to change
            Club_Member.objects.create(
                user=current_user,
                club=club_created,
                authorization='OW'
            )
            return redirect('members_list', club_created.id)
    else:
        form = CreateClubForm()
    return render(request, 'create_club.html', {'form': form})

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

    return render(request,'dashboard.html', {'other_clubs': other_clubs, 'my_clubs': my_clubs})

@login_required
def clubs_list(request, *args, **kwargs):
    clubs = get_all_clubs()
    if 'search_btn' in request.POST:
        if request.method == 'POST':
            searched_letters = request.POST['searched_letters']
            if searched_letters:
                clubs = get_clubs_search(searched_letters)

    if 'sort_table' in request.POST:
        if request.method == 'POST':
            sort_table = request.POST['sort_table']
            clubs = clubs.order_by(sort_table)

    return render(request, 'clubs_list.html', {'clubs': clubs})

@login_required
def show_club(request, *args, **kwargs):
    club = get_club(kwargs['club_id'])

    if club == None:
        return redirect('dashboard')

    owner = get_owners(club).first()

    return render(request, 'show_club.html', {'club_id': kwargs['club_id'], 'club': club, 'owner': owner, 'is_user_in_club': is_user_in_club(request.user, club)})

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
    for club in my_clubs:
        # In club table, delete all the request.users clubs where they are the only "person"
        count_all_users_in_club = get_count_of_users_in_club(club)
        if count_all_users_in_club == 1:
            club.delete()
            continue
        # In club table, delete where only applicants in club and 1 owner(the request user)
        if is_owner(request.user, club):
            count_applicants_in_club = get_count_of_specific_user_in_club(club, 'AP')
            if count_applicants_in_club + 1 == count_all_users_in_club:
                club.delete()

    # Delete the user from club_member and user table
    request.user.delete()
    messages.add_message(request, messages.SUCCESS, "Your account has been deleted")
    return redirect('home')
