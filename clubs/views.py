from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, UserUpdateForm, UserChangePasswordForm, LogInForm
from .models import User, Club

# Create your views here.
def home(request):
    return render(request,'home.html')

def sign_up(request):
    form = SignUpForm()
    return render(request,'sign_up.html',{'form': form})

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
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})


def members_list(request):
    applicants = Club.objects.filter(authorization='Applicant').values_list('user__id', flat=True)
    members = User.objects.exclude(id__in=applicants)
    return render(request, 'members_list.html', {'members': members})

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
