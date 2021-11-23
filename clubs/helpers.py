from django.core.exceptions import ObjectDoesNotExist
from django.db.models.functions import Concat
from django.db.models import Value
from .models import Club_Member, User

def get_all_users_except_applicants():
    applicants = Club_Member.objects.filter(authorization='Applicant').values_list('user__id', flat=True)
    members = User.objects.exclude(id__in=applicants)
    return members

def get_applicants():
    return get_users('AP')

def get_applicants_search(searched_letters):
    return get_users_search('AP', searched_letters)

def get_members():
    return get_users('ME')

def get_members_search(searched_letters):
    return get_users_search('ME', searched_letters)

def get_officers():
    return get_users('OF')

def get_officers_search(searched_letters):
    return get_users_search('OF', searched_letters)

def get_owners():
    return get_users('OW')

def get_users(search_authorization):
    authorizationFilter = (Club_Member.objects
        .filter(authorization=search_authorization)
        .values_list('user__id', flat=True))
    return User.objects.filter(id__in=authorizationFilter)

"""The idea of filter members with full name is from https://stackoverflow.com/questions/17932152/auth-filter-full-name"""
def get_users_search(search_authorization, searched_letters):
    searched_members = (User.objects
        .annotate(full_name=Concat('first_name', Value(' '), 'last_name'))
        .filter(full_name__icontains = searched_letters))
    return get_users(search_authorization).filter(id__in=searched_members)

def get_user(user_id):
    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return None
    return user

def get_authorization(user):
    try:
        authorization = (Club_Member.objects.get(user=user)).authorization
    except ObjectDoesNotExist:
        return None
    return authorization

def get_authorization_text(user):
    try:
        authorization_text = (Club_Member.objects.get(user=user)
            .get_authorization_display())
    except ObjectDoesNotExist:
        return None
    return authorization_text

def is_owner(user):
    if get_authorization(user) == 'OW':
        return True
    return False

def is_officer(user):
    if get_authorization(user) == 'OF':
        return True
    return False

def is_applicant(user):
    if get_authorization(user) == 'AP':
        return True
    return False
