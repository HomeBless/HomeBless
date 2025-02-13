from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from .models import Property, PropertyImage


# Create your views here.
class PropertyListing(ListView):
    model = Property
    template_name = 'property-listing.html'
    context_object_name = 'properties'

    def get_queryset(self):
        """Return only available properties sorted by newest"""
        properties = Property.objects.filter(is_available=True).order_by('-created_at')

        for property in properties:
            main_image = property.images.filter(is_main=True).first()
            if not main_image:
                main_image = property.images.first()
            property.main_image = main_image.image.url if main_image else None

        return properties

def property_list(request):
    properties = Property.objects.all()
    return render(request, 'property-listing.html', {'properties': properties})


class HomePage(TemplateView):
    template_name = 'homepage.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return redirect('HomeBless:homepage')


class Compare(TemplateView):
    template_name = 'compare.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return redirect('HomeBless:compare')


class PropertyDetail(TemplateView):
    template_name = 'property-detail.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return redirect('HomeBless:property-detail')
