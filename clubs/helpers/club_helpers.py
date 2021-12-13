from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from clubs.models import Club, Club_Member
from clubs.helpers.user_helpers import *
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

def get_club_to_auth(user, my_clubs):
    auth_list = []
    for club in my_clubs:
        auth_list.append(get_authorization_text(user, club))
    club_auth = list(zip(list(my_clubs), auth_list))
    return club_auth

def is_user_in_club(user, club):
    try:
        club_member = Club_Member.objects.get(user=user, club=club)
    except ObjectDoesNotExist:
        return False
    else:
        return True

def remove_user_from_club(user, club):
    """Remove the user in the club."""
    try:
        club_user = Club_Member.objects.get(user=user, club=club)
    except ObjectDoesNotExist:
        return None
    else:
        club_user.delete()

def remove_clubs(user, clubs):
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
                # at least one member or at least 1 officer in addition  to applicants and owner
                return (False, club.id)

    return (True,0)

def get_count_of_users_in_club(search_club):
    count = (Club_Member.objects
        .filter(club=search_club)
        .values_list('user__id', flat=True)
        .count())
    return count

def get_count_of_specific_user_in_club(search_club, search_authorization):
    count = (Club_Member.objects
        .filter(club=search_club)
        .filter(authorization=search_authorization)
        .values_list('user__id', flat=True)
        .count())
    return count
