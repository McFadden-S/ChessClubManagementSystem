from django.core.exceptions import ObjectDoesNotExist
from django.db.models.functions import Concat
from django.db.models import Value
from django.contrib import messages
from .models import Club, Club_Member, User

def get_clubs_search(searched_letters):
    """Get all the clubs that matches the searched letter from search bar."""

    searched_clubs = (Club.objects.filter(name__icontains = searched_letters))
    return get_all_clubs().filter(id__in=searched_clubs)

def get_applicants(club):
    """Get all the applicants from the given club."""

    return get_users(club, 'AP')

def get_members(club):
    """Get all the members from the given club."""

    return get_users(club, 'ME')

def get_officers(club):
    """Get all the officers from the given club."""

    return get_users(club, 'OF')

def get_owners(club):
    """Get all the owners from the given club."""

    return get_users(club, 'OW')

def get_users(search_club, search_authorization):
    """Get all the users from the given club with the given authorization."""

    authorizationFilter = (Club_Member.objects
        .filter(club=search_club)
        .filter(authorization=search_authorization)
        .values_list('user__id', flat=True))
    return User.objects.filter(id__in=authorizationFilter)

def get_user(user_id):
    """Get the user from the given user id."""

    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return None
    return user

def get_count_of_users_in_club(search_club):
    """Get the number of users in the given club."""

    count = (Club_Member.objects
        .filter(club=search_club)
        .values_list('user__id', flat=True)
        .count())
    return count

def get_count_of_specific_user_in_club(search_club, search_authorization):
    """Get the number of users in the given club with the given authorization."""

    count = (Club_Member.objects
        .filter(club=search_club)
        .filter(authorization=search_authorization)
        .values_list('user__id', flat=True)
        .count())
    return count

def get_authorization(user, club):
    """Get the authorization of a user in the given club."""

    if user is None or user.is_anonymous:
        return ""
    try:
        authorization = Club_Member.objects.filter(club=club).get(user=user).authorization
    except ObjectDoesNotExist:
        return None
    return authorization

def get_authorization_text(user, club):
    """Get the full text of the authorization of the given user in the given club."""

    try:
        authorization_text = (Club_Member.objects.filter(club=club).get(user=user)
                             .get_authorization_display())
    except ObjectDoesNotExist:
        return None
    return authorization_text

def set_authorization(user, club, authorization):
    """Set the authorization of the given user in the given club."""

    try:
        (Club_Member.objects
            .filter(user=user)
            .filter(club=club)
            .update(authorization=authorization))
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, "Cannot set authorization on a user that isnt apart of this club")

def is_owner(user, club):
    """Checks if a user is an owner in the given club."""

    if get_authorization(user, club) == 'OW':
        return True
    return False

def is_officer(user, club):
    """Checks if a user is an officer in the given club."""

    if get_authorization(user, club) == 'OF':
        return True
    return False

def is_member(user, club):
    """Checks if a user is a member in the given club."""

    if get_authorization(user, club) == 'ME':
        return True
    return False

def is_applicant(user, club):
    """Checks if a user is an applicant in the given club."""

    if get_authorization(user, club) == 'AP':
        return True
    return False

def get_club(club_id):
    """Get the club from the given club id."""

    try:
        club = Club.objects.get(id=club_id)
    except ObjectDoesNotExist:
        return None
    return club

def get_all_clubs():
    """Get all the existing clubs."""

    return Club.objects.all()

def get_my_clubs(user):
    """Get all the clubs the given user is in."""

    try:
        my_clubs_ids = Club_Member.objects.filter(user=user).values_list('club__id', flat=True)
        my_clubs = Club.objects.filter(id__in=my_clubs_ids)
    except ObjectDoesNotExist:
        return None
    return my_clubs

def get_other_clubs(user):
    """Get all other clubs the user is not in."""

    try:
        my_clubs = get_my_clubs(user)
        other_clubs = Club.objects.exclude(id__in=my_clubs)
    except ObjectDoesNotExist:
        return None
    return other_clubs

def get_club_to_auth(user, my_clubs):
    """Get the user authorization for eacn club the given user is in."""

    auth_list = []
    for club in my_clubs:
        auth_list.append(get_authorization_text(user, club))
    club_auth = list(zip(list(my_clubs), auth_list))
    return club_auth

def is_user_in_club(user, club):
    """Checks if the given user is in the given club."""

    try:
        club_member = Club_Member.objects.get(user=user, club=club)
    except ObjectDoesNotExist:
        return False
    else:
        return True

def remove_user_from_club(user, club):
    """Remove the user in the given club."""

    try:
        club_user = Club_Member.objects.get(user=user, club=club)
    except ObjectDoesNotExist:
        return None
    else:
        club_user.delete()

def remove_clubs(user, clubs):
    """Try to remove all the clubs the given user is in."""
    
    for club in clubs:
        # In club table, delete all the request.users clubs where they are the only "person"
        count_all_users_in_club = get_count_of_users_in_club(club)
        if count_all_users_in_club == 1:
            club.delete()
            continue
        # In club table, delete where only applicants in club and (the 1 owner(the request user) is only deleted)
        if is_owner(user, club):
            count_applicants_in_club = get_count_of_specific_user_in_club(club, 'AP')
            if count_applicants_in_club + 1 == count_all_users_in_club:
                club.delete()
            else:
                # at least one member or at least 1 officer in addition to applicants and owner
                return (False, club.id)

    return (True,0)
