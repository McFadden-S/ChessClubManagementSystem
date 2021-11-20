from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect,render
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, UserUpdateForm, UserChangePasswordForm, LogInForm
from .models import User, Club
from django.contrib.auth.hashers import check_password

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
    applicants = Club.objects.filter(authorization='AP').values_list('user__id', flat=True)
    members = User.objects.exclude(id__in=applicants)
    return render(request, 'members_list.html', {'members': members})

def only_officer(view_func):
    def modified_view_func(request):
        if (Club.objects.get(user=request.user)).authorization != 'OF':
            return redirect('home')
        else:
            return view_func(request)
    return modified_view_func

@only_officer
def applicants_list(request):
    applicants_list = Club.objects.filter(authorization='AP').values_list('user__id', flat=True)
    applicants = User.objects.filter(id__in=applicants_list)
    return render(request, 'applicants_list.html', {'applicants':applicants})


def approve_applicant(request, applicant_id):
    applicant = User.objects.get(id=applicant_id)
    Club.objects.filter(user=applicant).update(authorization="ME")
    return redirect('applicants_list')


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
