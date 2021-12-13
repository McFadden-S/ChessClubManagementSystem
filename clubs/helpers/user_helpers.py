from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from clubs.models import User, Club_Member

def get_user(user_id):
    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return None
    return user

def get_users(search_club, search_authorization):
    authorizationFilter = (Club_Member.objects
        .filter(club=search_club)
        .filter(authorization=search_authorization)
        .values_list('user__id', flat=True))
    return User.objects.filter(id__in=authorizationFilter)

def get_applicants(club):
    return get_users(club, 'AP')

def is_applicant(user, club):
    if get_authorization(user, club) == 'AP':
        return True
    return False

def get_members(club):
    return get_users(club, 'ME')

def is_member(user, club):
    if get_authorization(user, club) == 'ME':
        return True
    return False

def get_officers(club):
    return get_users(club, 'OF')

def is_officer(user, club):
    if get_authorization(user, club) == 'OF':
        return True
    return False

def get_owners(club):
    return get_users(club, 'OW')

def is_owner(user, club):
    if get_authorization(user, club) == 'OW':
        return True
    return False

def get_authorization(user, club):
    if user is None or user.is_anonymous:
        return ""
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
