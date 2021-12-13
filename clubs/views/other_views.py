from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormView
from django.views.generic import TemplateView

from clubs.forms import *
from clubs.models import *
from clubs.helpers import *
from .mixins import *

class HomeView(LoginProhibitedMixin, TemplateView):
    """View that allows user to choose to sign up or log in."""

    template_name = 'home.html'

class CreateClubView(LoginRequiredMixin, FormView):
    """View to create a club"""

    template_name = "create_club.html"
    form_class = CreateClubForm

    def form_valid(self,form):
        """Proccess the form."""

        current_user = self.request.user
        try:
            # Create the club with the owner being the user who filled the form.
            club_created = form.save()
            Club_Member.objects.create(user=current_user, club=club_created, authorization='OW')
            messages.success(self.request, "Club created Successfully")
            return super().form_valid(form)
        except IndexError:
            # Render the form again if the address is invalid
            messages.error(self.request, "Invalid address")
            form_new = CreateClubForm()
            return render(self.request,'create_club.html',{'form': form_new})

    def get_success_url(self):
        """Return redirect URL to dashboard after creating a club successfully."""

        return reverse('dashboard')

class WaitingListView(ApplicantsOnlyMixin, TemplateView):
    """ View for the waiting list for applicants to a club """

    template_name = 'waiting_list.html'

    def get_context_data(self, **kwargs):
        """Generate context data to be shown in the template."""

        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        club = get_club(kwargs['club_id'])

        context['my_clubs'] = get_my_clubs(current_user)
        context['my_authorization'] = get_authorization_text(current_user, club)

        return context
