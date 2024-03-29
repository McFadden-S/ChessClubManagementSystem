"""Views for account-related purposes."""
from clubs.forms import *
from clubs.helpers import *
from clubs.views.mixins import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, reverse,render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, UpdateView



class SignUpView(LoginProhibitedMixin, FormView):
    """View that signs up user."""

    form_class = SignUpForm
    template_name = "sign_up.html"

    def form_valid(self, form):
        """Proccess the form."""

        self.object = form.save()
        login(self.request, self.object)
        messages.success(self.request, f"Your account was created successfully")
        return super().form_valid(form)

    def get_success_url(self):
        """Return redirect URL to dashboard after successfully registering an account."""

        return reverse('dashboard')

class LogInView(LoginProhibitedMixin, FormView):
    """View to log in to the system."""

    template_name = "log_in.html"
    form_class = LogInForm

    def form_valid(self, form):
        """Proccess the form."""

        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)

        if user is None:
            form = LogInForm()
            messages.error(self.request, "Incorrect login")
            return render(self.request, 'log_in.html',  {'form':form})

        login(self.request, user)
        messages.success(self.request, "Login Successful")
        return super().form_valid(form)

    def get_success_url(self):
        """Return redirect URL to dashboard after logging in successfully."""

        redirect_next = self.request.POST.get('next') or None
        if(redirect_next):
            return redirect_next
        return reverse('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        redirect_next = self.request.GET.get('next') or None
        if(redirect_next):
            context['next'] = redirect_next

        return context

class LogOutView(LoginRequiredMixin, TemplateView):
    """View to log out of the system."""

    def get(self, request, *args, **kwargs):
        """Handle get request."""

        logout(request)
        messages.success(self.request, "Logged out successfully")
        return redirect('home')

class UpdateUserView(LoginRequiredMixin, UpdateView):
    """View to update logged-in user's profile."""

    model = UpdateUserForm
    template_name = "user_update.html"
    form_class = UpdateUserForm

    def get_object(self):
        """Return the object (user) to be updated."""

        user = self.request.user
        return user

    def get_context_data(self, **kwargs):
        """Generate context data to be shown in the template."""

        context = super().get_context_data(**kwargs)
        context['my_clubs'] = get_my_clubs(self.request.user)

        return context

    def get_success_url(self):
        """Return redirect URL to dashboard after successful update."""

        messages.success(self.request, "User Information Updated Successfully")
        return reverse('dashboard')

class ChangePasswordView(LoginRequiredMixin, FormView):
    """View to change logged-in user's password."""

    template_name = "change_password.html"
    form_class = UserChangePasswordForm

    def form_valid(self, form):
        """Ensure form is valid"""

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
        """Generate context data to be shown in the template."""

        context = super().get_context_data(**kwargs)
        context['my_clubs'] = get_my_clubs(self.request.user)

        return context

    def get_success_url(self):
        """Return redirect URL to dashboard after changing the password successfully."""

        return reverse('dashboard')
