from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect, reverse
from django.contrib import messages

from clubs.forms import *
from clubs.helpers import *
from .mixins import *

from django.contrib.auth.decorators import login_required
from clubs.decorators import *

class SignUpView(LoginProhibitedMixin, FormView):
    """View that signs up user."""

    form_class = SignUpForm
    template_name = "sign_up.html"

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        messages.success(self.request, f"Your account was created successfully")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('dashboard')

class LogInView(LoginProhibitedMixin, FormView):
    """View to log in to the system."""

    template_name = "log_in.html"
    form_class = LogInForm

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)

        if user is None:
            return super().form_invalid(form)

        login(self.request, user)
        messages.success(self.request, "Login Successful")
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('dashboard')

class UpdateUserView(LoginRequiredMixin, UpdateView):
    """View to update logged-in user's profile."""

    model = UserUpdateForm
    template_name = "user_update.html"
    form_class = UserUpdateForm

    def get_object(self):
        """Return the object (user) to be updated."""
        user = self.request.user
        return user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_clubs'] = get_my_clubs(self.request.user)

        return context

    def get_success_url(self):
        """Return redirect URL after successful update."""
        messages.success(self.request, "User Information Updated Successfully")
        return reverse('dashboard')

class ChangePasswordView(LoginRequiredMixin, FormView):
    """View to change logged-in user's password."""

    template_name = "change_password.html"
    form_class = UserChangePasswordForm

    def form_valid(self, form):
        current_user = self.request.user
        password = form.cleaned_data.get('password')

        if check_password(password, current_user.password):
            new_password = form.cleaned_data.get('new_password')
            current_user.set_password(new_password)
            current_user.save()
            login(self.request, current_user)

            messages.success(self.request, "Password Changed Successfully")
            return super().form_valid(form)

        else:
            return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_clubs'] = get_my_clubs(self.request.user)

        return context

    def get_success_url(self):
        return reverse('dashboard')

@login_required
def log_out(request):
    logout(request)
    return redirect('home')

@login_required
def delete_account(request):
    my_clubs = get_my_clubs(request.user)
    if remove_clubs(request.user, my_clubs)[0] == False:
        messages.add_message(request, messages.ERROR, "You must transfer ownership before you delete account for club")
        return redirect('members_list', remove_clubs(request.user, my_clubs)[1])


    # Delete the user from club_member and user table
    request.user.delete()
    messages.add_message(request, messages.SUCCESS, "Your account has been deleted")
    return redirect('home')
