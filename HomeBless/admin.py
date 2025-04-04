from django.contrib import admin
from .models import Property


class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'location', 'is_available', 'created_at', 'user')
    list_filter = ('is_available', 'selling_type', 'seller_status', 'property_type')
    search_fields = ('title', 'location', 'description')
    list_editable = ('is_available',)

    actions = ['make_available', 'make_unavailable']

    def make_available(self, request, queryset):
        """Mark selected properties as available for sale"""
        queryset.update(is_available=True)
        self.message_user(request, "Selected properties are now marked as available.")

    def make_unavailable(self, request, queryset):
        """Mark selected properties as unavailable for sale"""
        queryset.update(is_available=False)
        self.message_user(request, "Selected properties are now marked as unavailable.")

    make_available.short_description = "Mark selected as available"
    make_unavailable.short_description = "Mark selected as unavailable"


admin.site.register(Property, PropertyAdmin)
