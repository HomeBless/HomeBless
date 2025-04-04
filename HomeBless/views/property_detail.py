from django.shortcuts import redirect
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Property, Wishlist


class PropertyDetail(DetailView):
    model = Property
    template_name = 'property-detail.html'
    context_object_name = 'property'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        property = self.object

        context['user_is_authenticated'] = self.request.user.is_authenticated

        # Main Image and Extra Images
        main_image = property.images.filter(is_main=True).first() or property.images.first()
        extra_images = property.images.exclude(id=main_image.id) if main_image else property.images.all()

        # Add attributes to the property object
        property.main_image = main_image.image.url if main_image else None
        property.extra_images = extra_images
        property.price_per_area = float(property.price) / float(property.area) if property.area else 0

        # Related Properties
        related_properties = Property.objects.filter(is_available=True).exclude(id=property.id)[:4]
        for prop in related_properties:
            prop_main_image = prop.images.filter(is_main=True).first() or prop.images.first()
            prop.main_image = prop_main_image.image.url if prop_main_image else None

        # Handle wishlist for authenticated users only
        wishlist_bool = False
        if self.request.user.is_authenticated:
            wishlist_bool = Wishlist.objects.filter(user=self.request.user, property=property).exists()

        # Seller Information
        seller_name = self.get_seller_short_name()
        seller_status = property.get_seller_status_display()
        seller_phone = property.phone_number
        seller_line_id = property.line_id
        seller_email = property.contact_email
        selling_type = property.get_selling_type_display()

        # Update context
        context.update({
            'related_properties': related_properties,
            'wishlist_bool': wishlist_bool,
            'seller_name': seller_name,
            'seller_status': seller_status,
            'seller_phone': seller_phone,
            'seller_line_id': seller_line_id,
            'seller_email': seller_email,
            'selling_type': selling_type,
            **self.get_property_tags()
        })

        return context

    def get_seller_short_name(self):
        """Get seller name as 'First LastInitial.'"""
        user = self.object.user
        if user.get_full_name():
            full_name = user.get_full_name()
            name_parts = full_name.split()
            if len(name_parts) > 1:
                first_name = name_parts[0]
                last_initial = name_parts[-1][0]
                return f"{first_name} {last_initial}."
            return full_name
        return user.username

    def get_property_tags(self):
        """Get tags related to the property."""
        property = self.object
        return {
            # Decoration
            'decoration_tags': property.decoration.all(),
            'flooring_tags': property.flooring.all(),
            'wall_tags': property.wall_type.all(),
            'ceiling_tags': property.ceiling_type.all(),

            # Home Features
            'home_features_tags': property.home_features.all(),

            # Project Amenities
            'security_tags': property.security.all(),
            'common_area_tags': property.common_area.all(),
            'travelling_tags': property.travelling.all(),
            'facility_tags': property.facilities.all(),

            # System in the House
            'home_system_tags': property.home_systems.all(),

            # Additional Property Conditions
            'condition_tags': property.conditions.all(),
            'view_tags': property.views.all(),
            'warranty_tags': property.warranties.all(),
        }

    def post(self, request, *args, **kwargs):
        """Toggle property in wishlist."""
        if not request.user.is_authenticated:
            return redirect('HomeBless:login')

        property = self.get_object()
        wishlist_item = Wishlist.objects.filter(user=request.user, property=property).first()

        if wishlist_item:
            wishlist_item.delete()
        else:
            Wishlist.objects.create(user=request.user, property=property)

        return redirect('HomeBless:property-detail', pk=property.pk)