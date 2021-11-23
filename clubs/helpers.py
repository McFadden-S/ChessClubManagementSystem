from .models import Club_Member, User
from django.core.exceptions import ObjectDoesNotExist

def get_all_users_except_applicants():
    applicants = Club_Member.objects.filter(authorization='Applicant').values_list('user__id', flat=True)
    members = User.objects.exclude(id__in=applicants)
    return members

def get_applicants():
    return get_users_by_authorization('AP')

def get_members():
    return get_users_by_authorization('ME')

def get_officers():
    return get_users_by_authorization('OF')

def get_owners():
    return get_users_by_authorization('OW')

def get_users_by_authorization(search_authorization):
    authorizationFilter = Club_Member.objects.filter(authorization=search_authorization).values_list('user__id', flat=True)
    user = User.objects.filter(id__in=authorizationFilter)
    return user

def get_authorization(user):
    try:
        authorization = (Club_Member.objects.get(user=user)).authorization
    except ObjectDoesNotExist:
        return None
    return authorization
