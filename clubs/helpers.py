from django.core.exceptions import ObjectDoesNotExist
from django.db.models.functions import Concat
from django.db.models import Value
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from .models import Club, Club_Member, User

# havent seen this being used.
# def get_all_users_except_applicants():
#     applicants = (Club_Member.objects.filter(authorization='Applicant')
#                                      .values_list('user__id', flat=True))
#     members = User.objects.exclude(id__in=applicants)
#     return members

def get_clubs_search(searched_letters):
    searched_clubs = (Club.objects.filter(name__icontains = searched_letters))
    return get_all_clubs().filter(id__in=searched_clubs)

def get_applicants(club):
    return get_users(club, 'AP')

def get_applicants_search(search_club, searched_letters):
    return get_users_search(search_club, 'AP', searched_letters)

def get_members(club):
    return get_users(club, 'ME')

def get_members_search(search_club, searched_letters):
    return get_users_search(search_club, 'ME', searched_letters)

def get_officers(club):
    return get_users(club, 'OF')

def get_officers_search(search_club, searched_letters):
    return get_users_search(search_club, 'OF', searched_letters)

def get_owners(club):
    return get_users(club, 'OW')

def get_owners_search(search_club, searched_letters):
    return get_users_search(search_club, 'OW', searched_letters)

def get_users(search_club, search_authorization):
    authorizationFilter = (Club_Member.objects
        .filter(club=search_club)
        .filter(authorization=search_authorization)
        .values_list('user__id', flat=True))
    return User.objects.filter(id__in=authorizationFilter)

def get_users_search(search_club, search_authorization, searched_letters):
    searched_members = (User.objects
        .annotate(full_name=Concat('first_name', Value(' '), 'last_name'))
        .filter(full_name__icontains = searched_letters))
    result = get_users(search_club, search_authorization).filter(id__in=searched_members)
    return result

def get_user(user_id):
    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return None
    return user
# havent seen this being used.
# def get_user_of_club(user_id, club):
#     try:
#         user = User.objects.get(id=user_id)
#
#         #below will through an ObjectDoesNotExist if not apart of club
#         Club_Member.objects.filter(club=club).get(user=user)
#     except ObjectDoesNotExist:
#         return None
#     return user

def get_authorization(user, club):
    try:
        authorization = Club_Member.objects.filter(club=club).get(user=user).authorization
    except ObjectDoesNotExist:
        return None
    return authorization

def get_authorization_text(user, club):
    try:
        authorization_text = (Club_Member.objects.filter(club=club).get(user=user)
                             .get_authorization_display())
    except ObjectDoesNotExist:
        return None
    return authorization_text

def set_authorization(user, club, authorization):
    try:
        (Club_Member.objects
            .filter(user=user)
            .filter(club=club)
            .update(authorization=authorization))
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, "Cannot set authorization on a user that isnt apart of this club")

def is_owner(user, club):
    if get_authorization(user, club) == 'OW':
        return True
    return False

def is_officer(user, club):
    if get_authorization(user, club) == 'OF':
        return True
    return False

def is_member(user, club):
    if get_authorization(user, club) == 'ME':
        return True
    return False

def is_applicant(user, club):
    if get_authorization(user, club) == 'AP':
        return True
    return False

def get_club(club_id):
    try:
        club = Club.objects.get(id=club_id)
    except ObjectDoesNotExist:
        return None
    return club

def get_all_clubs():
    return Club.objects.all()

def get_my_clubs(user):
    try:
        my_clubs_ids = Club_Member.objects.filter(user=user).values_list('club__id', flat=True)
        my_clubs = Club.objects.filter(id__in=my_clubs_ids)
    except ObjectDoesNotExist:
        return None
    return my_clubs

def get_other_clubs(user):
    try:
        my_clubs = get_my_clubs(user)
        other_clubs = Club.objects.exclude(id__in=my_clubs)
    except ObjectDoesNotExist:
        return None
    return other_clubs

def is_user_in_club(user, club):
    try:
        club_member = Club_Member.objects.get(user=user, club=club)
    except ObjectDoesNotExist:
        return False
    else:
        return True
