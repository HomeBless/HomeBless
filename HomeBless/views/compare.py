from django.shortcuts import render
from django.views.generic import TemplateView
from ..models.wishlist import Wishlist, Property


class Compare(TemplateView):
    template_name = 'compare.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        property_id = request.GET.get("property_id")
        main_property = Property.objects.filter(id=property_id).first()
        context['main_id'] = property_id

        if main_property:
            context.update({
                'main_title': main_property,
                'main_area': main_property.area,
                'main_floor': main_property.floors,
                'main_bedroom': main_property.bedrooms,
                'main_bathroom': main_property.bathrooms,
                'main_price': main_property.price,
                'main_price_per_wa': main_property.price / main_property.area if main_property.area else None,
                'main_type': main_property.property_type.name if main_property.property_type else None,
            })

        radius_km = int(request.GET.get("radius", 10))
        transaction_type = request.GET.get("type", "sell")

        if request.user.is_authenticated:
            wishlist_items = Wishlist.objects.filter(user=request.user).select_related('property')
            context['wishlist_properties'] = [
                {
                    **vars(item.property),
                    'price_per_wa': item.property.price / item.property.area if item.property.area else None
                }
                for item in wishlist_items
            ]

        return render(request, self.template_name, context)
