from django.shortcuts import redirect

class LoginProhibitedMixin():

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('members_list')
        return super().dispatch(*args, **kwargs)
