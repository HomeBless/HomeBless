from django.shortcuts import redirect
from django.views.generic import ListView

from ..models import Property, Wishlist


class PropertyListing(ListView):
    model = Property
    template_name = 'property-listing.html'
    context_object_name = 'properties'

    def get_queryset(self):
        """Return only available properties sorted by newest"""
        properties = Property.objects.filter(is_available=True)  # .order_by('-created_at')

        for property in properties:
            main_image = property.images.filter(is_main=True).first()
            if not main_image:
                main_image = property.images.first()
            property.main_image = main_image.image.url if main_image else None

        return properties

    def post(self, request, *args, **kwargs):
        """Toggle property in wishlist."""
        print("All POST data:", request.POST)

        property_id = request.POST.get('property_id')

        # Debug the received property_id
        print('Received property_id:', property_id)

        property = Property.objects.get(pk=property_id)

        print('property:', property)

        user = request.user

        print('property:', property)
        print('user:', user)

        wishlist_item = Wishlist.objects.filter(user=user, property=property).first()
        if wishlist_item:
            wishlist_item.delete()
        else:
            Wishlist.objects.create(user=user, property=property)

        return redirect('HomeBless:property-listing')
