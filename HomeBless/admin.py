from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group, User
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken

from .models import Property

# Admin customization
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_available', 'created_at')
    readonly_fields = [field.name for field in Property._meta.fields if field.name != 'is_available']
    actions = ['mark_as_approved', 'mark_as_disapproved']

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [field.name for field in self.model._meta.fields if field.name != 'is_available']
        return super().get_readonly_fields(request, obj)

    def save_model(self, request, obj, form, change):
        if change:
            original = Property.objects.get(pk=obj.pk)
            if original.is_available and not obj.is_available:
                obj.is_available = True
        super().save_model(request, obj, form, change)

    @admin.action(description="Approve Selected Property(ies)")
    def mark_as_approved(self, request, queryset):
        updated = queryset.update(is_available=True)
        self.message_user(request, f"{updated} property(ies) marked as approved.")

    @admin.action(description="Reject Selected Properties")
    def mark_as_disapproved(self, request, queryset):
        updated = queryset.update(is_available=False)
        self.message_user(request, f"{updated} property(ies) marked as disapproved.")

# Unregister built-in and third-party models
unregister_models = [Site, Group, User, EmailAddress, SocialAccount, SocialApp, SocialToken]

for model in unregister_models:
    if model in admin.site._registry:
        admin.site.unregister(model)

# Register only Property
admin.site.register(Property, PropertyAdmin)

# Custom branding
admin.site.site_header = "Homebless Administration"
admin.site.site_title = "Homebless Admin Portal"
admin.site.index_title = "Welcome to Homebless Admin"
