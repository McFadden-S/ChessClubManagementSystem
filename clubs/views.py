from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'home.html')

def sign_up(request):
    return render(request,'sign_up.html')
