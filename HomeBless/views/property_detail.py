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
        universities = self.get_nearby_places("","มหาวิทยาลัย")
        filtered_universities = [uni for uni in universities if uni["name"].startswith("มหาวิทยาลัย")][:2]
        context["nearby_university"] = filtered_universities
        schools = self.get_nearby_places("secondary_school", "")
        filtered_schools = [school for school in schools if
                                 school["name"].startswith("โรงเรียน")][:2]
        context['nearby_school'] = filtered_schools
        airports = self.get_nearby_places("สนามบิน", "สนามบิน")
        filtered_airports = [airport for airport in airports if
                                 airport["name"].startswith("ท่าอากาศยาน")][:2]
        context['nearby_airport'] = filtered_airports
        context['nearby_mall'] = self.get_nearby_places("shopping_mall" ,"ศูนย์การค้า")[:3]
        hospitals = self.get_nearby_places("hospital", "โรงพยาบาล")
        filtered_hospitals = [hospital for hospital in hospitals if hospital["name"].startswith("โรงพยาบาล")][:2]
        context['nearby_hospital'] = filtered_hospitals
        transports = self.get_nearby_places("สถานีรถไฟฟ้า", "สถานีรถไฟฟ้า")
        filtered_transports = [transport for transport in transports
                               if transport["name"] in
                               ["คูคต", "แยก คปอ.", "พิพิธภัณฑ์กองทัพอากาศ",
                                "โรงพยาบาลภูมิพลอดุลยเดช", "สะพานใหม่", "สายหยุด",
                                "พหลโยธิน 59", "วัดพระศรีมหาธาตุ", "กรมทหารราบที่ 11",
                                "บางบัว", "กรมป่าไม้", "มหาวิทยาลัยเกษตรศาสตร์",
                                "เสนานิคม", "รัชโยธิน", "พหลโยธิน 24", "ห้าแยกลาดพร้าว",
                                "หมอชิต", "สะพานควาย", "อารีย์", "สนามเป้า", "อนุสาวรีย์ชัยสมรภูมิ",
                                "พญาไท", "ราชเทวี", "สยาม", "ชิดลม", "เพลินจิต", "นานา", "อโศก",
                                "พร้อมพงษ์", "ทองหล่อ", "เอกมัย", "พระโขนง", "อ่อนนุช",
                                "บางจาก", "ปุณณวิถี", "อุดมสุข", "บางนา", "แบริ่ง", "สำโรง", "ปู่เจ้า",
                                "ช้างเอราวัณ", "โรงเรียนนายเรือ", "ปากน้ำ", "ศรีนครินทร์",
                                "แพรกษา", "สายลวด", "เคหะฯ", "สนามกีฬาแห่งชาติ",
                                "ราชดำริ", "ศาลาแดง", "ช่องนนทรี", "เซนต์หลุยส์", "สุรศักดิ์",
                                "สะพานตากสิน", "กรุงธนบุรี", "วงเวียนใหญ่", "โพธิ์นิมิตร",
                                "ตลาดพลู", "วุฒากาศ", "บางหว้า", "เจริญนคร (ไอคอนสยาม)",
                                "คลองสาน", "ท่าพระ", "จรัญฯ 13", "ไฟฉาย", "บางขุนนนท์",
                                "บางยี่ขัน", "สิรินธร", "บางพลัด", "บางอ้อ", "บางโพ",
                                "เตาปูน", "บางซื่อ", "กำแพงเพชร", "สวนจตุจักร", "พหลโยธิน",
                                "ลาดพร้าว", "รัชดาภิเษก", "สุทธิสาร", "ห้วยขวาง", "ศูนย์วัฒนธรรมแห่งประเทศไทย",
                                "พระราม 9", "เพชรบุรี", "สุขุมวิท", "ศูนย์การประชุมแห่งชาติสิริกิติ์",
                                "คลองเตย", "ลุมพินี", "สามย่าน", "หัวลำโพง", "วัดมังกร",
                                "สามยอด", "สนามไชย", "อิสรภาพ", "บางไผ่", "เพชรเกษม 48",
                                "ภาษีเจริญ", "บางแค", "หลักสอง", "รังสิต", "หลักหก (มหาวิทยาลัยรังสิต)",
                                "ดอนเมือง", "การเคหะ", "หลักสี่", "ทุ่งสองห้อง", "บางเขน",
                                "วัดเสมียนนารี", "กรุงเทพอภิวัฒน์", "คลองบางไผ่", "ตลาดบางใหญ่",
                                "สามแยกบางใหญ่", "บางพลู", "บางรักใหญ่", "บางรักน้อยท่าอิฐ",
                                "ไทรม้า", "สะพานพระนั่งเกล้า", "แยกนนทบุรี 1", "บางกระสอ",
                                "กระทรวงสาธารณสุข", "แยกติวานนท์", "วงศ์สว่าง", "บางซ่อน"]][:2]
        context['nearby_transport'] = filtered_transports

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

    def get_nearby_places(self, type, keyword):
        """Fetch nearby places using Google Places API."""
        lat = self.object.latitude
        lng = self.object.longitude
        google_api_key = settings.GOOGLE_MAPS_API_KEY

        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&rankby=distance&type={type}&keyword={keyword}&language=th&key={google_api_key}"
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
