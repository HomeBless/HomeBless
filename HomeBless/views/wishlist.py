from django.shortcuts import render, redirect
from django.template import context
from django.views.generic import TemplateView
from ..models import Wishlist


class WishlistView(TemplateView):
    template_name = 'wishlist.html'
    context_object_name = 'wishlist'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all wishlist items for the user
        wishlist = Wishlist.objects.filter(user=request.user)
        context['wishlist'] = wishlist

        # Prepare additional data for each wishlist item
        wishlist_details = []
        for item in wishlist:
            property = item.property
            wishlist_details.append({
                'id': property.id,
                'picture': property.images.filter(is_main=True).first() or property.images.first(),
                'title': property.title,
                'price': property.price,
                'floor': property.floors,
                'bedrooms': property.bedrooms,
                'bathrooms': property.bathrooms,
            })

        context['wishlist_details'] = wishlist_details

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        property_id = request.POST.get('property_id')
        user = request.user

        wishlist_item = Wishlist.objects.filter(user=user, property_id=property_id)

        if wishlist_item:
            wishlist_item.delete()

        return redirect('HomeBless:wishlist')

