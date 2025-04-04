from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView

from ..models import Property, PropertyImage, PropertyType


class PropertyManage(LoginRequiredMixin, TemplateView):
    template_name = 'property-manage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_properties = Property.objects.filter(user=self.request.user)
        context['properties'] = user_properties
        context['property_types'] = PropertyType.objects.all()

        # Get main images for current user's properties
        main_images = PropertyImage.objects.filter(
            property__in=user_properties, is_main=True
        )

        # Convert to dict: {property_id: image}
        cover_images = {img.property_id: img for img in main_images}
        context['cover_images'] = cover_images

        return context

    def post(self, request, *args, **kwargs):
        property_id = request.POST.get('delete_property_id')
        if property_id:
            property_instance = get_object_or_404(
                Property, id=property_id, user=request.user
            )
            property_instance.delete()
        return redirect('HomeBless:manage')
