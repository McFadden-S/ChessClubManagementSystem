from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect,render
from .forms import SignUpForm, UserUpdateForm, UserChangePasswordForm, LogInForm
from .models import User, Club

# Create your views here.
def home(request):
    return render(request,'home.html')

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Club.objects.create(user=user)
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
            if user is not None:
                login(request, user)
                redirect_url = 'members_list'
                return redirect(redirect_url)
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid")
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('home')

def members_list(request):
    member_list = Club.objects.filter(authorization='ME').values_list('user__id', flat=True)
    members = User.objects.filter(id__in=member_list)
    officer_list = Club.objects.filter(authorization='OF').values_list('user__id', flat=True)
    officers = User.objects.filter(id__in=officer_list)
    current_user = request.user
    cu_auth = (Club.objects.get(user=current_user)).authorization
    is_owner = False
    if cu_auth == 'OW':
        is_owner = True
    return render(request, 'members_list.html', {'members': members, 'officers': officers, 'is_owner': is_owner})

def show_member(request, member_id):
    try:
        member = User.objects.get(id=member_id)
        auth = (Club.objects.get(user=member)).authorization
    except ObjectDoesNotExist:
        return redirect('member_list')
    else:
        return render(request, 'show_member.html',
            {'member': member, 'auth' : auth}
        )

def promote_member(request, member_id):
    member = User.objects.get(id=member_id)
    auth = (Club.objects.get(user=member)).authorization
    if auth == 'ME':
        Club.objects.filter(user=member).update(authorization="OF")
        return redirect(members_list)
    else:
        return render(request, 'member_list.html',
            {'member': member, 'auth' : auth}
        )
