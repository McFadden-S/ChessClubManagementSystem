from django.conf import settings
from django.shortcuts import redirect
from .helpers import get_authorization, get_club
from django.contrib import messages

# not using
# def login_prohibited(view_function):
#     def modified_view_function(request):
#         if request.user.is_authenticated:
#             return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
#         else:
#             return view_function(request)
#     return modified_view_function

# not using
# def only_applicants(view_func):
#     def modified_view_func(request, *args, **kwargs):
#         authorization = get_authorization(request.user, get_club(kwargs['club_id']))
#         if not request.user.is_authenticated:
#             return redirect('log_in')
#         if authorization == None:
#             messages.add_message(request, messages.ERROR, "You are not an applicant")
#             return redirect('dashboard')
#         elif authorization == 'AP':
#             return view_func(request, *args, **kwargs)
#         else:
#             messages.add_message(request, messages.ERROR, "You are not an applicant")
#             return redirect('members_list', kwargs['club_id'])
#     return modified_view_func

def only_members(view_func):
    def modified_view_func(request, *args, **kwargs):
        authorization = get_authorization(request.user, get_club(kwargs['club_id']))
        if not request.user.is_authenticated:
            return redirect('log_in')
        if authorization == None:
            messages.add_message(request, messages.ERROR, "You are not a member/owner/officer")
            return redirect('dashboard')
        elif authorization == 'AP':
            messages.add_message(request, messages.ERROR, "You are not a member/owner/officer")
            return redirect('waiting_list', kwargs['club_id'])
        else:
            return view_func(request, *args, **kwargs)
    return modified_view_func

def only_officers(view_func):
    def modified_view_func(request, *args, **kwargs):
        authorization = get_authorization(request.user, get_club(kwargs['club_id']))
        if not request.user.is_authenticated:
            return redirect('log_in')
        if authorization == None:
            messages.add_message(request, messages.ERROR, "You are not an owner/officer")
            return redirect('dashboard')
        elif authorization == 'AP':
            messages.add_message(request, messages.ERROR, "You are not an owner/officer")
            return redirect('waiting_list', kwargs['club_id'])
        elif authorization == 'ME':
            messages.add_message(request, messages.ERROR, "You are not an owner/officer")
            return redirect('members_list', kwargs['club_id'])
        else:
            return view_func(request, *args, **kwargs)
    return modified_view_func

def only_owners(view_func):
    def modified_view_func(request, *args, **kwargs):
        authorization = get_authorization(request.user, get_club(kwargs['club_id']))
        if not request.user.is_authenticated:
            return redirect('log_in')
        if authorization == None:
            messages.add_message(request, messages.ERROR, "You are not an owner")
            return redirect('dashboard')
        elif authorization == 'AP':
            messages.add_message(request, messages.ERROR, "You are not an owner")
            return redirect('waiting_list', kwargs['club_id'])
        elif authorization == 'ME' or authorization == 'OF':
            messages.add_message(request, messages.ERROR, "You are not an owner")
            return redirect('members_list', kwargs['club_id'])
        else:
            return view_func(request, *args, **kwargs)
    return modified_view_func
