def only_officer_and_owner(view_func):
    def modified_view_func(request, **kwargs):
        try:
            Club_Member.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return redirect('members_list')
        authorization = (Club_Member.objects.get(user=request.user)).authorization
        if authorization == 'AP':
            return redirect('waiting_list')
        if authorization == 'ME':
            return redirect('members_list')
        else:
            appId = 0;
            for (key, value) in kwargs.items():
                appId = value
            return view_func(request,appId)
    return modified_view_func

def only_members(view_func):
    def modified_view_func(request):
        try:
            Club_Member.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return redirect('log_in')
        authorization = (Club_Member.objects.get(user=request.user)).authorization
        if authorization != 'ME' or authorization != 'OF' or authorization != 'OW':
            return redirect('home')
        else:
            return view_func(request)
    return modified_view_func

def only_members(view_func):
    def modified_view_func(request):
        try:
            Club_Member.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return redirect('log_in')
        authorization = (Club_Member.objects.get(user=request.user)).authorization
        if authorization != 'ME' or authorization != 'OF' or authorization != 'OW':
            return redirect('home')
        else:
            return view_func(request)
    return modified_view_func

def getAllMembersExceptApplicants():
    applicants = Club_Member.objects.filter(authorization='Applicant').values_list('user__id', flat=True)
    members = User.objects.exclude(id__in=applicants)
    return members

def getMembers():
    memberFilter = Club_Member.objects.filter(authorization='Member').values_list('user__id', flat=True)
    members = User.objects.filter(id__in=memberFilter)
    return members

def getOfficers():
    officerFilter = Club_Member.objects.filter(authorization='Officer').values_list('user__id', flat=True)
    officers = User.objects.filter(id__in=officerFilter)
    return officers

def _getAuthorization(user):
    try:
        authorization = (Club_Member.objects.get(user=user)).authorization
    except ObjectDoesNotExist:
        return None
    return authorization
