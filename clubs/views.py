from django.shortcuts import redirect,render
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, UserUpdateForm, UserChangePasswordForm, LogInForm

# Create your views here.
def home(request):
    return render(request,'home.html')

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
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
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})
