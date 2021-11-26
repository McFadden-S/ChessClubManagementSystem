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

from .forms import *
from .models import *
from .helpers import *
from .decorators import *
from .mixins import *

# Create your views here.
@login_prohibited
def home(request):
    return render(request,'home.html')

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
            messages.success(self.request, f"Your password was changed successfully")
            login(self.request, current_user)
            return super().form_valid(form)

        else:
            return super().form_invalid(form)

    def get_success_url(self):
        return reverse('dashboard')

@login_required
@only_applicants
def waiting_list(request, club_id):
    return render(request,'waiting_list.html', {'club_id' : club_id})

@login_prohibited
def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                redirect_url = 'dashboard'
                return redirect(redirect_url)

        messages.add_message(request, messages.ERROR, "The credentials provided were invalid")
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})

@login_required
def log_out(request):
    logout(request)
    return redirect('home')

@login_required
@only_members
def members_list(request, club_id):
    club = get_club(club_id)
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

    return render(request, 'members_list.html', {'club_id': club_id, 'members': members, 'officers': officers, 'owners': owners})

@login_required
@only_members
def show_member(request, club_id, member_id):
    club = get_club(club_id)
    member = get_user(member_id)
    authorizationText = get_authorization_text(member, club)

    if member == None or authorizationText == None:
        return redirect('dashboard')

    return render(request, 'show_member.html',
        {'club_id': club_id,
        'member': member,
        'authorizationText' : authorizationText,
        'request_from_owner' : is_owner(request.user, club),
        'request_from_officer' : is_officer(request.user, club)})

@login_required
@only_officers
def applicants_list(request, club_id, *args):
    club = get_club(club_id)
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

    return render(request, 'applicants_list.html', {'club_id' : club_id, 'applicants': applicants})

@login_required
@only_officers
def show_applicant(request, club_id, applicant_id):
    club = get_club(club_id)
    applicant = get_user(applicant_id)

    if applicant == None or not is_applicant(applicant, club):
        return redirect('applicants_list', club_id)

    return render(request, 'show_applicant.html',
        {'club_id' : club_id, 'applicant': applicant})

@login_required
@only_officers
def approve_applicant(request, club_id, applicant_id):
    club = get_club(club_id)
    current_user = request.user
    applicant = get_user(applicant_id)
    if (is_officer(current_user, club) or is_owner(current_user, club)) and is_applicant(applicant, club):
        set_authorization(applicant, club, "ME")
        return redirect('applicants_list', club_id)
    return render(request, 'applicants_list.html', {'club_id' : club_id, 'applicants': applicants})

@login_required
@only_owners
def promote_member(request, club_id, member_id):
    club = get_club(club_id)
    current_user = request.user
    member = get_user(member_id)
    if is_owner(current_user, club) and is_member(member, club):
        set_authorization(member, club, "OF")
        return redirect(members_list, club_id)
    return render(request, 'members_list.html',
        {'club_id': club_id, 'member': member, 'auth' : get_authorization(current_user, club)})

@login_required
@only_owners
def demote_officer(request, club_id, member_id):
    club = get_club(club_id)
    current_user = request.user
    member = get_user(member_id)
    if is_owner(current_user, club) and is_officer(member, club):
        set_authorization(member, club, "ME")
        return redirect(members_list, club_id)
    return render(request, 'members_list.html',
        {'club_id': club_id, 'member': member, 'auth' : get_authorization(current_user, club)})

@login_required
@only_owners
def transfer_ownership(request, club_id, member_id):
    club = get_club(club_id)
    current_user = request.user
    member = get_user(member_id)
    if is_owner(current_user, club) and is_officer(member, club):
        set_authorization(member, club, "OW")
        set_authorization(current_user, club, "OF")
        return redirect(members_list, club_id)
    return render(request, 'members_list.html',
        {'club_id': club_id, 'member': member, 'auth' : get_authorization(current_user, club)})

@login_required
def create_club(request):
    if request.method == 'POST':
        current_user = request.user
        form = CreateClubForm(request.POST)
        if form.is_valid():
            club_created = form.save()
            # redirect link needs to change
            Club_Member.objects.create(
                user=current_user,
                club=club_created,
                authorization='OF'
            )
            return redirect('members_list', club_created.id)
    else:
        form = CreateClubForm()
    return render(request, 'create_club.html', {'form': form})

@login_required
def dashboard(request):
    current_user = request.user
    my_clubs = get_my_clubs(current_user)
    other_clubs = get_other_clubs(current_user)
    return render(request,'dashboard.html', {'other_clubs': other_clubs, 'my_clubs': my_clubs})

@login_required
def clubs_list(request, *args):
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
