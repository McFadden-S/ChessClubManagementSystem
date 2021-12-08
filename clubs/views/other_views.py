from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect,render
from django.urls import reverse
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.views import View

from clubs.forms import *
from clubs.models import *
from clubs.helpers import *
from .mixins import *

from django.contrib.auth.decorators import login_required

class HomeView(LoginProhibitedMixin, TemplateView):
    template_name = 'home.html'

class CreateClubView(LoginRequiredMixin, FormView):
    template_name = "create_club.html"
    form_class = CreateClubForm

    def form_valid(self,form):
        current_user = self.request.user
        try:
            club_created = form.save()
            Club_Member.objects.create(user=current_user, club=club_created, authorization='OW')
            messages.success(self.request, "Club created Successfully")
            return super().form_valid(form)
        except IndexError:
            messages.error(self.request, "Invalid address")
            form_new = CreateClubForm()
            return render(self.request,'create_club.html',{'form': form_new})

    def get_success_url(self):
        return reverse('dashboard')

class WaitingListView(ApplicantsOnlyMixin, TemplateView):
    """ View for the waiting list for applicants to a club """

    template_name = 'waiting_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user

        context['my_clubs'] = get_my_clubs(current_user)
        club = get_club(kwargs['club_id'])
        context['my_authorization'] = get_authorization_text(current_user, club)

        return context

@login_required
def dashboard(request, *args, **kwargs):
    current_user = request.user
    my_clubs = get_my_clubs(current_user)
    other_clubs = get_other_clubs(current_user)

    if 'search_btn' in request.POST:
        if request.method == 'POST':
            searched_letters = request.POST['searched_letters']
            if searched_letters:
                my_clubs = get_clubs_search(searched_letters)
                other_clubs = get_clubs_search(searched_letters)

    if 'sort_table' in request.POST:
        if request.method == 'POST':
            sort_table = request.POST['sort_table']
            my_clubs = my_clubs.order_by(sort_table)
            other_clubs = other_clubs.order_by(sort_table)

    club_auth = get_club_to_auth(current_user, my_clubs)
    return render(request,'dashboard.html', {'other_clubs': other_clubs, 'my_clubs': my_clubs, 'club_auth': club_auth})
