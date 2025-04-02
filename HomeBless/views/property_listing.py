from django.views.generic import ListView

from ..models import Property

class PropertyListing(ListView):
    model = Property
    template_name = 'property-listing.html'
    context_object_name = 'properties'

    def get_queryset(self):
        """Return only available properties sorted by newest"""
        properties = Property.objects.filter(is_available=True) #.order_by('-created_at')

        for property in properties:
            main_image = property.images.filter(is_main=True).first()
            if not main_image:
                main_image = property.images.first()
            property.main_image = main_image.image.url if main_image else None

        return properties