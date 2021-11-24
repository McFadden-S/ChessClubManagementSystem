from django.conf import settings
from django.shortcuts import redirect
from .helpers import get_authorization
from django.contrib import messages

def login_prohibited(view_function):
    def modified_view_function(request):
        if request.user.is_authenticated:
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        else:
            return view_function(request)
    return modified_view_function

def only_applicants(view_func):
    def modified_view_func(request, **kwargs):
        authorization = get_authorization(request.user)
        if authorization == None:
            return redirect('log_in')
        elif authorization == 'AP':
            return view_func(request, **kwargs)
        else:
            messages.add_message(request, messages.ERROR, "You are not an applicant")
            return redirect('members_list')
    return modified_view_func

def only_members(view_func):
    def modified_view_func(request, **kwargs):
        authorization = get_authorization(request.user)
        if authorization == None:
            return redirect('log_in')
        elif authorization == 'AP':
            messages.add_message(request, messages.ERROR, "You are not a member/owner/officer")
            return redirect('waiting_list')
        else:
            return view_func(request, **kwargs)
    return modified_view_func

def only_officers(view_func):
    def modified_view_func(request, **kwargs):
        authorization = get_authorization(request.user)
        if authorization == None:
            return redirect('log_in')
        elif authorization == 'AP':
            messages.add_message(request, messages.ERROR, "You are not an owner/officer")
            return redirect('waiting_list')
        elif authorization == 'ME':
            messages.add_message(request, messages.ERROR, "You are not an owner/officer")
            return redirect('members_list')
        else:
            return view_func(request, **kwargs)
    return modified_view_func

def only_owners(view_func):
    def modified_view_func(request, **kwargs):
        authorization = get_authorization(request.user)
        if authorization == None:
            return redirect('log_in')
        elif authorization == 'AP':
            messages.add_message(request, messages.ERROR, "You are not an owner")
            return redirect('waiting_list')
        elif authorization == 'ME' or authorization == 'OF':
            messages.add_message(request, messages.ERROR, "You are not an owner")
            return redirect('members_list')
        else:
            return view_func(request, **kwargs)
    return modified_view_func
