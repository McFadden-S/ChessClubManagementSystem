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
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('waiting_list')

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
        return reverse('members_list')

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
            return super().form_valid(form)

        else:
            return super().form_invalid(form)

    def get_success_url(self):
        return reverse('members_list')

@login_required
@only_applicants
def waiting_list(request):
    return render(request,'waiting_list.html')

@login_prohibited
def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            user_authorization = get_authorization(user)
            if user_authorization == 'AP':
                login(request, user)
                return redirect('waiting_list')
            elif user is not None:
                login(request, user)
                redirect_url = 'members_list'
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
def members_list(request):

    members = get_members()
    officers = get_officers()
    owners = get_owners()

    if request.method == 'POST':
        searched_letters = request.POST['searched_letters']
        if searched_letters:
            members = get_members_search(searched_letters)
            officers = get_officers_search(searched_letters)

    return render(request, 'members_list.html', {'members': members, 'officers': officers, 'owners': owners})

@login_required
@only_members
def show_member(request, member_id):
    member = get_user(member_id)
    authorizationText = get_authorization_text(member)

    if member == None or authorizationText == None:
        return redirect('members_list')

    return render(request, 'show_member.html',
        {'member': member,
        'authorizationText' : authorizationText,
        'request_from_owner' : is_owner(request.user),
        'request_from_officer' : is_officer(request.user)})

@login_required
@only_officers
def applicants_list(request, *args):

    applicants = get_applicants()

    if request.method == 'POST':
        searched_letters = request.POST['searched_letters']
        if searched_letters:
            applicants = get_applicants_search(searched_letters)

    return render(request, 'applicants_list.html', {'applicants':applicants})

@login_required
@only_officers
def show_applicant(request, applicant_id):
    applicant = get_user(applicant_id)

    if applicant == None or not is_applicant(applicant):
        return redirect('applicants_list')

    return render(request, 'show_applicant.html',
        {'applicant': applicant})

@login_required
@only_officers
def approve_applicant(request, applicant_id):
    applicant = User.objects.get(id=applicant_id)
    Club_Member.objects.filter(user=applicant).update(authorization="ME")
    return redirect('applicants_list')

@login_required
@only_owners
def promote_member(request, member_id):
    current_user = request.user
    cu_auth = (Club_Member.objects.get(user=current_user)).authorization
    member = User.objects.get(id=member_id)
    auth = (Club_Member.objects.get(user=member)).authorization
    is_owner = False
    if cu_auth == 'OW':
        is_owner = True
    if is_owner:
        if auth == 'ME':
            Club_Member.objects.filter(user=member).update(authorization="OF")
            return redirect(members_list)
    else:
        return render(request, 'members_list.html',
            {'member': member, 'auth' : auth}
        )

@login_required
@only_owners
def demote_officer(request, member_id):
    current_user = request.user
    cu_auth = (Club_Member.objects.get(user=current_user)).authorization
    member = User.objects.get(id=member_id)
    auth = (Club_Member.objects.get(user=member)).authorization
    is_owner = False
    if cu_auth == 'OW':
        is_owner = True
    if is_owner:
        if auth == 'OF':
            Club_Member.objects.filter(user=member).update(authorization="ME")
            return redirect(members_list)
    else:
        return render(request, 'members_list.html',
            {'member': member, 'auth' : auth}
        )

@login_required
@only_owners
def transfer_ownership(request, member_id):
    current_user = request.user
    cu_auth = (Club_Member.objects.get(user=current_user)).authorization
    member = User.objects.get(id=member_id)
    auth = (Club_Member.objects.get(user=member)).authorization
    is_owner = False
    if cu_auth == 'OW':
        is_owner = True
    if is_owner:
        if auth == 'OF':
            Club_Member.objects.filter(user=member).update(authorization="OW")
            Club_Member.objects.filter(user=current_user).update(authorization="OF")
            return redirect(members_list)
    else:
        return render(request, 'members_list.html',
            {'member': member, 'auth' : auth}
        )
