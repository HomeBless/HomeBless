from django.shortcuts import render
from django.views.generic import TemplateView
from ..models.wishlist import Wishlist, Property
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

            radius = request.GET.get("radius")
            try:
                radius = int(radius)
            except (TypeError, ValueError):
                radius = 10  # default to 10 km

            selling_type = request.GET.get("selling_type", main_property.selling_type)
            all_properties = Property.objects.exclude(id=main_property.id) \
                .exclude(latitude=None) \
                .exclude(longitude=None) \
                .filter(selling_type=selling_type)


            nearby_cheapest = self.get_lowest_nearby(main_property, radius, all_properties)
            if nearby_cheapest:
                context['cheapest_nearby'] = nearby_cheapest

            nearby_highest = self.get_highest_nearby(main_property, radius, all_properties)
            if nearby_highest:
                context['highest_nearby'] = nearby_highest

            nearby_closest = self.get_nearest_price_per_wa_nearby(main_property, radius, all_properties)
            if nearby_closest:
                context['closest_nearby'] = nearby_closest

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

    def get_lowest_nearby(self, main_property, max_km, all_properties):
        matrix_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        destinations = [f"{p.latitude},{p.longitude}" for p in all_properties]

        highest_property = None
        lowest_price_per_wa = None

        for i in range(0, len(destinations), 25):  # Batch size due to API limits
            batch = destinations[i:i+25]
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
                            if prop.area:
                                price_per_wa = prop.price / prop.area
                                if lowest_price_per_wa is None or price_per_wa < lowest_price_per_wa:
                                    highest_property = prop
                                    lowest_price_per_wa = price_per_wa

        if highest_property:
            return {
                'title': highest_property.title,
                'price': highest_property.price,
                'area': highest_property.area,
                'price_per_wa': round(lowest_price_per_wa, 2),
                'lat': highest_property.latitude,
                'lon': highest_property.longitude,
                'type': highest_property.property_type,
                'floor': highest_property.floors,
                'bedrooms': highest_property.bedrooms,
                'bathrooms': highest_property.bathrooms
            }

        return None

    def get_highest_nearby(self, main_property, max_km, all_properties):
        matrix_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        destinations = [f"{p.latitude},{p.longitude}" for p in all_properties]

        best_property = None
        highest_price_per_wa = None

        for i in range(0, len(destinations),
                       25):  # Batch size due to API limits
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
                            if prop.area:
                                price_per_wa = prop.price / prop.area
                                if highest_price_per_wa is None or price_per_wa > highest_price_per_wa:
                                    best_property = prop
                                    highest_price_per_wa = price_per_wa

        if best_property:
            return {
                'title': best_property.title,
                'price': best_property.price,
                'area': best_property.area,
                'price_per_wa': round(highest_price_per_wa, 2),
                'lat': best_property.latitude,
                'lon': best_property.longitude,
                'type': best_property.property_type,
                'floor': best_property.floors,
                'bedrooms': best_property.bedrooms,
                'bathrooms': best_property.bathrooms
            }

        return None

    def get_nearest_price_per_wa_nearby(self, main_property, max_km, all_properties):
        matrix_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        destinations = [f"{p.latitude},{p.longitude}" for p in all_properties]

        main_price_per_wa = main_property.price / main_property.area if main_property.area else None
        if main_price_per_wa is None:
            return None

        closest_match_property = None
        smallest_price_diff = None

        for i in range(0, len(destinations), 25):  # Google API batch limit
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
                            if prop.area:
                                price_per_wa = prop.price / prop.area
                                diff = abs(price_per_wa - main_price_per_wa)
                                if smallest_price_diff is None or diff < smallest_price_diff:
                                    closest_match_property = prop
                                    smallest_price_diff = diff

        if closest_match_property:
            return {
                'title': closest_match_property.title,
                'price': closest_match_property.price,
                'area': closest_match_property.area,
                'price_per_wa': round(
                    closest_match_property.price / closest_match_property.area,
                    2),
                'lat': closest_match_property.latitude,
                'lon': closest_match_property.longitude,
                'type': closest_match_property.property_type,
                'floor': closest_match_property.floors,
                'bedrooms': closest_match_property.bedrooms,
                'bathrooms': closest_match_property.bathrooms
            }

        return None

    @csrf_exempt
    def set_wishlist_property(request):
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                property_id = data.get('property_id')

                # Save property ID to session
                request.session['wishlist_property_id'] = property_id
                return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)},
                                    status=400)

        return JsonResponse(
            {'success': False, 'error': 'Invalid request method'}, status=405)
