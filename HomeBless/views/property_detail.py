import requests
from django.shortcuts import redirect
from django.views.generic import DetailView
from ..models import Property
from django.conf import settings


class PropertyDetail(DetailView):
    model = Property
    template_name = 'property-detail.html'
    context_object_name = 'property'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Main Image and Extra Images
        main_image = self.object.images.filter(is_main=True).first() or self.object.images.first()
        extra_images = self.object.images.exclude(id=main_image.id) if main_image else self.object.images.all()

        # Add attributes to the property object
        self.object.main_image = main_image.image.url if main_image else None
        self.object.extra_images = extra_images
        self.object.price_per_area = float(self.object.price) / float(self.object.area)

        # Related Properties
        related_properties = Property.objects.filter(is_available=True).exclude(id=self.object.id)
        for property in related_properties:
            property_main_image = property.images.filter(is_main=True).first() or property.images.first()
            property.main_image = property_main_image.image.url if property_main_image else None

        context['related_properties'] = related_properties

        # Seller Information
        context['seller_name'] = self.get_seller_short_name()
        context['seller_status'] = self.object.get_seller_status_display()
        context['seller_phone'] = self.object.phone_number
        context['seller_line_id'] = self.object.line_id
        context['seller_email'] = self.object.contact_email
        context['selling_type'] = self.object.get_selling_type_display()

        # Map API
        context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY

        # Nearby Places (Multiple Types)
        universities = self.get_nearby_places("มหาวิทยาลัย")
        filtered_universities = [uni for uni in universities if uni["name"].startswith("มหาวิทยาลัย")][:2]
        context["nearby_university"] = filtered_universities
        schools = self.get_nearby_places("secondary_school")
        filtered_schools = [school for school in schools if
                                 school["name"].startswith("โรงเรียน")][:2]
        context['nearby_school'] = filtered_schools
        airports = self.get_nearby_places("สนามบิน")
        filtered_airports = [airport for airport in airports if
                                 airport["name"].startswith("ท่าอากาศยาน")][:2]
        context['nearby_airport'] = filtered_airports
        context['nearby_mall'] = self.get_nearby_places("ศูนย์การค้า")[:3]
        context['nearby_hospital'] = self.get_nearby_places("โรงพยาบาล")[:2]
        context['nearby_transport'] = self.get_nearby_places("สถานีรถไฟฟ้า")[:2]

        # Decoration and Home Features
        context.update(self.get_property_tags())

        return context

    def get_seller_short_name(self):
        """Get seller name as 'First LastInitial.'"""
        full_name = self.object.user.get_full_name()
        name_parts = full_name.split()
        if len(name_parts) > 1:
            first_name = name_parts[0]
            last_initial = name_parts[-1][0]
            return f"{first_name} {last_initial}."
        return full_name

    def get_property_tags(self):
        """Get tags related to the property."""
        return {
            # Decoration
            'decoration_tags': self.object.decoration.all(),
            'flooring_tags': self.object.flooring.all(),
            'wall_tags': self.object.wall_type.all(),
            'ceiling_tags': self.object.ceiling_type.all(),

            # Home Features
            'home_features_tags': self.object.home_features.all(),

            # Project Amenities
            'security_tags': self.object.security.all(),
            'common_area_tags': self.object.common_area.all(),
            'travelling_tags': self.object.travelling.all(),
            'facility_tags': self.object.facilities.all(),

            # System in the House
            'home_system_tags': self.object.home_systems.all(),

            # Additional Property Conditions
            'condition_tags': self.object.conditions.all(),
            'view_tags': self.object.views.all(),
            'warranty_tags': self.object.warranties.all(),
        }

    def get_nearby_places(self, keyword):
        """Fetch nearby places using Google Places API."""
        lat = 13.84814
        lng = 100.57223
        google_api_key = settings.GOOGLE_MAPS_API_KEY

        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&rankby=distance&keyword={keyword}&language=th&key={google_api_key}"
        response = requests.get(url)
        data = response.json()

        places = [
            {
                "name": place.get("name"),
                "place_id": place.get("place_id"),
                "location": f"{place['geometry']['location']['lat']},{place['geometry']['location']['lng']}",
                "distance": '',
            }
            for place in data.get("results", [])
        ]

        # Prepare the destinations for the Distance Matrix API
        destinations = "|".join([place["location"] for place in places])
        distance_url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={lat},{lng}&destinations={destinations}&key={google_api_key}&language=th"

        distance_response = requests.get(distance_url)
        distance_data = distance_response.json()

        # Add the distance data to the places list
        for index, element in enumerate(
            distance_data.get("rows", [])[0].get("elements", [])):
            if "distance" in element:
                places[index]["distance"] = element["distance"].get("text",
                                                                    "N/A")

        return places

    def post(self, request, *args, **kwargs):
        return redirect('HomeBless:property-detail', pk=self.get_object().pk)
