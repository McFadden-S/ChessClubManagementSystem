from django.views.generic import TemplateView
from django.shortcuts import render

class PageNotFoundView(TemplateView):
    """ View for when page is not found """

    template_name = '404.html'

    def render(request, exception):
        return render(request, template_name, status=404)

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)
