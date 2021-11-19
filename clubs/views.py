from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from .forms import SignUpForm
from .forms import LogInForm

# Create your views here.
def home(request):
    return render(request,'home.html')

def sign_up(request):
    form = SignUpForm()
    return render(request,'sign_up.html',{'form': form})

def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                redirect_url = 'home'
                return redirect(redirect_url)
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid")
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})
