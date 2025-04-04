from django.shortcuts import render, redirect
from django.template import context
from django.views.generic import TemplateView
from ..models import Wishlist, PropertyImage


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
            prop = item.property
            main_image = PropertyImage.objects.filter(property=prop, is_main=True).first()
            fallback_image = PropertyImage.objects.filter(property=prop).first()

            wishlist_details.append({
                'id': prop.id,
                'picture': main_image or fallback_image,
                'title': prop.title,
                'price': prop.price,
                'floor': prop.floors,
                'bedrooms': prop.bedrooms,
                'bathrooms': prop.bathrooms,
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

