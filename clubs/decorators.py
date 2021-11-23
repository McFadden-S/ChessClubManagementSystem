from django.conf import settings
from django.shortcuts import redirect
from .helpers import get_authorization

def login_prohibited(view_function):
    def modified_view_function(request):
        if request.user.is_authenticated:
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        else:
            return view_function(request)
    return modified_view_function

def only_officers(view_func):
    def modified_view_func(request, **kwargs):
        authorization = get_authorization(request.user)
        if authorization == None:
            return redirect('log_in')
        if authorization == 'AP':
            return redirect('waiting_list')
        if authorization == 'ME':
            return redirect('members_list')
        else:
            return view_func(request, **kwargs)
    return modified_view_func

def only_members(view_func):
    def modified_view_func(request, **kwargs):
        authorization = get_authorization(request.user)
        if authorization == None:
            return redirect('log_in')
        if authorization == 'AP':
            return redirect('waiting_list')
        else:
            return view_func(request, **kwargs)
    return modified_view_func
