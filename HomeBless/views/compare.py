from django.shortcuts import render
from django.views.generic import TemplateView
from ..models import Wishlist, Property, PropertyImage
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import requests
from django.conf import settings


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
                'main_price_per_wa': round(main_property.price / main_property.area, 2) if main_property.area else None,
                'main_type': main_property.property_type.name if main_property.property_type else None,
                'main_lat': main_property.latitude,
                'main_lon': main_property.longitude
            })

            # Attach main image
            main_image = PropertyImage.objects.filter(property=main_property, is_main=True).first()
            context['main_image_url'] = main_image.image.url if main_image else None

            radius = request.GET.get("radius")
            try:
                radius = int(radius)
            except (TypeError, ValueError):
                radius = 10

            selling_type = request.GET.get("selling_type", main_property.selling_type)
            all_properties = Property.objects.exclude(id=main_property.id) \
                .exclude(latitude=None).exclude(longitude=None) \
                .filter(selling_type=selling_type)

            def get_image_url(prop):
                img = PropertyImage.objects.filter(property=prop, is_main=True).first()
                return img.image.url if img else None

            nearby_cheapest = self.get_lowest_nearby(main_property, radius, all_properties)
            if nearby_cheapest:
                nearby_cheapest['image_url'] = get_image_url(nearby_cheapest['instance'])
                context['cheapest_nearby'] = nearby_cheapest

            nearby_highest = self.get_highest_nearby(main_property, radius, all_properties)
            if nearby_highest:
                nearby_highest['image_url'] = get_image_url(nearby_highest['instance'])
                context['highest_nearby'] = nearby_highest

            nearby_closest = self.get_nearest_price_per_wa_nearby(main_property, radius, all_properties)
            if nearby_closest:
                nearby_closest['image_url'] = get_image_url(nearby_closest['instance'])
                context['closest_nearby'] = nearby_closest

        if request.user.is_authenticated:
            wishlist_items = Wishlist.objects.filter(user=request.user).select_related('property')
            context['wishlist_properties'] = [
                {
                    **vars(item.property),
                    'price_per_wa': item.property.price / item.property.area if item.property.area else None
                } for item in wishlist_items
            ]

        return render(request, self.template_name, context)

    def get_lowest_nearby(self, main_property, max_km, all_properties):
        return self._find_nearby(main_property, max_km, all_properties, lowest=True)

    def get_highest_nearby(self, main_property, max_km, all_properties):
        return self._find_nearby(main_property, max_km, all_properties, highest=True)

    def get_nearest_price_per_wa_nearby(self, main_property, max_km, all_properties):
        return self._find_nearby(main_property, max_km, all_properties, closest=True)

    def _find_nearby(self, main_property, max_km, all_properties, lowest=False, highest=False, closest=False):
        matrix_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        destinations = [f"{p.latitude},{p.longitude}" for p in all_properties]

        main_price_per_wa = main_property.price / main_property.area if main_property.area else None
        result = None
        best_value = None

        for i in range(0, len(destinations), 25):
            batch = destinations[i:i + 25]
            response = requests.get(matrix_url, params={
                "origins": f"{main_property.latitude},{main_property.longitude}",
                "destinations": "|".join(batch),
                "key": settings.GOOGLE_MAPS_API_KEY,
                "units": "metric"
            })

            data = response.json()
            if data['status'] == 'OK':
                for idx, element in enumerate(data['rows'][0]['elements']):
                    if element['status'] == 'OK':
                        distance_km = element['distance']['value'] / 1000.0
                        if distance_km <= max_km:
                            prop = all_properties[i + idx]
                            if not prop.area:
                                continue

                            price_per_wa = prop.price / prop.area
                            if lowest:
                                if best_value is None or price_per_wa < best_value:
                                    result = prop
                                    best_value = price_per_wa
                            elif highest:
                                if best_value is None or price_per_wa > best_value:
                                    result = prop
                                    best_value = price_per_wa
                            elif closest:
                                diff = abs(price_per_wa - main_price_per_wa)
                                if best_value is None or diff < best_value:
                                    result = prop
                                    best_value = diff

        if result:
            return {
                'title': result.title,
                'price': result.price,
                'area': result.area,
                'price_per_wa': round(result.price / result.area, 2),
                'lat': result.latitude,
                'lon': result.longitude,
                'type': result.property_type,
                'floor': result.floors,
                'bedrooms': result.bedrooms,
                'bathrooms': result.bathrooms,
                'instance': result
            }
        return None

    @csrf_exempt
    def set_wishlist_property(request):
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                property_id = data.get('property_id')
                request.session['wishlist_property_id'] = property_id
                return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)}, status=400)

        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
