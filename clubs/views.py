from django.shortcuts import render
from .forms import SignUpForm, userUpdateForm, userChangePasswordForm
# Create your views here.
def home(request):
    return render(request,'home.html')

def sign_up(request):
    form = SignUpForm()
    return render(request,'sign_up.html',{'form': form})

def change_password(request):
    pass

def update_user(request):
    pass
