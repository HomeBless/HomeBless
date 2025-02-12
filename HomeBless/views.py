from django.shortcuts import render, redirect
from django.views.generic import TemplateView


# Create your views here.
class PropertyListing(TemplateView):
    template_name = 'property-listing.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return redirect('HomeBless:property-listing')

