from django.shortcuts import render
from .forms import LogInForm

# Create your views here.
def home(request):
    return render(request,'home.html')

def log_in(request):
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})
