from django.shortcuts import redirect
from django.conf import settings

class LoginProhibitedMixin():

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        return super().dispatch(*args, **kwargs)
