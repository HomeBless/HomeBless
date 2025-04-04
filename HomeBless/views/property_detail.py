from django.shortcuts import redirect
from django.views.generic import DetailView
from ..models import Property, Wishlist


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

        context['wishlist_bool'] = Wishlist.objects.filter(user=self.request.user, property=self.object).exists()

        # Seller Information
        context['seller_name'] = self.get_seller_short_name()
        context['seller_status'] = self.object.get_seller_status_display()
        context['seller_phone'] = self.object.phone_number
        context['seller_line_id'] = self.object.line_id
        context['seller_email'] = self.object.contact_email
        context['selling_type'] = self.object.get_selling_type_display()

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

    def post(self, request, *args, **kwargs):
        """Toggle property in wishlist."""
        property = self.get_object()
        user = request.user

        wishlist_item = Wishlist.objects.filter(user=user, property=property).first()

        if wishlist_item:
            wishlist_item.delete()
        else:
            Wishlist.objects.create(user=user, property=property)

        return redirect('HomeBless:property-detail', pk=property.pk)

