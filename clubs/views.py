from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect,render
from .forms import SignUpForm, UserUpdateForm, UserChangePasswordForm, LogInForm
from .models import User, Club_Member
from django.contrib.auth.hashers import check_password
from django.db.models.functions import Concat
from django.db.models import Value
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def home(request):
    return render(request,'home.html')

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Club_Member.objects.create(user=user)
            return redirect('waiting_list')
    else:
        form = SignUpForm()
    return render(request,'sign_up.html',{'form': form})

def waiting_list(request):
    return render(request,'waiting_list.html')

@login_required
def update_user(request):
    current_user = request.user
    if request.method == 'POST':
        form = UserUpdateForm(instance=current_user, data=request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, "User Information updated!")
            form.save()
    else:
        form = UserUpdateForm(instance=current_user)
    return render(request, 'user_update.html', {'form': form})

@login_required
def change_password(request):
    current_user = request.user
    if request.method == 'POST':
        form = UserChangePasswordForm(data=request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            if check_password(password, current_user.password):
                new_password = form.cleaned_data.get('new_password')
                current_user.set_password(new_password)
                current_user.save()
                messages.add_message(request, messages.SUCCESS, "Password updated!")
    form = UserChangePasswordForm()
    return render(request, 'change_password.html', {'form': form})

def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            user_authorization = _getAuthorization(user)
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

def log_out(request):
    logout(request)
    return redirect('home')

def only_officer(view_func):
    def modified_view_func(request, **kwargs):
        try:
            Club_Member.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return redirect('members_list')
        if (Club_Member.objects.get(user=request.user)).authorization != 'OF':
            return redirect('members_list')
        else:
            appId = 0;
            for (key, value) in kwargs.items():
                appId = value
            return view_func(request,appId)
    return modified_view_func

def only_officer_and_owner(view_func):
    def modified_view_func(request, **kwargs):
        try:
            Club_Member.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return redirect('members_list')
        authorization = (Club_Member.objects.get(user=request.user)).authorization
        if authorization == 'AP':
            return redirect('waiting_list')
        if authorization == 'ME':
            return redirect('members_list')
        else:
            appId = 0;
            for (key, value) in kwargs.items():
                appId = value
            return view_func(request,appId)
    return modified_view_func

def only_members(view_func):
    def modified_view_func(request):
        try:
            Club_Member.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return redirect('log_in')
        authorization = (Club_Member.objects.get(user=request.user)).authorization
        if authorization != 'ME' or authorization != 'OF' or authorization != 'OW':
            return redirect('home')
        else:
            return view_func(request)
    return modified_view_func

"""The idea of filter members with full name is from https://stackoverflow.com/questions/17932152/auth-filter-full-name"""
#@only_members TODO: LOG IN NEEDS TO REDIRECT SOMEWHERE ELSE FOR THIS TO BE UNCOMMENTED
@login_required
def members_list(request):
    member_list = Club_Member.objects.filter(authorization='ME').values_list('user__id', flat=True)
    members = User.objects.filter(id__in=member_list)
    officer_list = Club_Member.objects.filter(authorization='OF').values_list('user__id', flat=True)
    officers = User.objects.filter(id__in=officer_list)
    if request.method == 'POST':
        searched_letters = request.POST['searched_letters']
        if searched_letters:
            searched_members = User.objects.annotate(
                full_name=Concat('first_name', Value(' '), 'last_name')
            ).filter(full_name__icontains = searched_letters)
            members = members.filter(id__in=searched_members)
            officers = officers.filter(id__in=searched_members)
    return render(request, 'members_list.html', {'members': members, 'officers': officers})

@login_required
@only_officer_and_owner
def applicants_list(request, *args):
    applicants_list = Club_Member.objects.filter(authorization='AP').values_list('user__id', flat=True)
    applicants = User.objects.filter(id__in=applicants_list)
    if request.method == 'POST':
        searched_letters = request.POST['searched_letters']
        if searched_letters:
            searched_members = User.objects.annotate(
                full_name=Concat('first_name', Value(' '), 'last_name')
            ).filter(full_name__icontains = searched_letters)
            applicants = applicants.filter(id__in=searched_members)
    return render(request, 'applicants_list.html', {'applicants':applicants})

@login_required
@only_officer_and_owner
def approve_applicant(request, applicant_id):
    applicant = User.objects.get(id=applicant_id)
    Club_Member.objects.filter(user=applicant).update(authorization="ME")
    return redirect('applicants_list')

@login_required
@only_officer_and_owner
def show_applicant(request, applicant_id):
    try:
        Club_Member.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return redirect('members_list')
    try:
        applicant = User.objects.get(id=applicant_id)
    except ObjectDoesNotExist:
        return redirect('applicants_list')
    else:
        # THE APPLICANT HAS ALREADY BEEN APPROVED CASE
        if (Club_Member.objects.get(user=applicant)).authorization != 'AP':
            return redirect('applicants_list')
        return render(request, 'show_applicant.html',
            {'applicant': applicant}
        )

@login_required
#@only_members TODO change when log in redirects to general landing page
def show_member(request, member_id):
    try:
        member = User.objects.get(id=member_id)
        authorizationText = (Club_Member.objects.get(user=member)).get_authorization_display()
        request_from_owner = False
        request_from_officer = False
        current_user = request.user
        #PLEASE ADD THIS IN A TRY BLOCK OR USE _getAuthorization()
        cu_auth = (Club_Member.objects.get(user=current_user)).authorization
        if cu_auth == 'OW':
            request_from_owner = True
        elif cu_auth == 'OF':
            request_from_officer = True
    except ObjectDoesNotExist:
        return redirect('members_list')
    else:
        return render(request, 'show_member.html',
            {'member': member,
            'authorizationText' : authorizationText,
            'request_from_owner' : request_from_owner,
            'request_from_officer' : request_from_officer}
        )

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

def getAllMembersExceptApplicants():
    applicants = Club_Member.objects.filter(authorization='Applicant').values_list('user__id', flat=True)
    members = User.objects.exclude(id__in=applicants)
    return members

def _getAuthorization(user):
    try:
        authorization = (Club_Member.objects.get(user=user)).authorization
    except ObjectDoesNotExist:
        return None
    return authorization
