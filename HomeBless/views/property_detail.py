from django.shortcuts import redirect
from django.views.generic import DetailView
from ..models import Property

class PropertyDetail(DetailView):
    model = Property
    template_name = 'property-detail.html'
    context_object_name = 'property'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the main image (if marked) or fallback to the first available image
        main_image = self.object.images.filter(is_main=True).first()
        if not main_image:
            main_image = self.object.images.first()

        # Get extra images excluding the main image
        extra_images = self.object.images.exclude(id=main_image.id) if main_image else self.object.images.all()

        # Add attributes to the property object
        self.object.main_image = main_image.image.url if main_image else None
        self.object.extra_images = extra_images
        self.object.price_per_area = float(self.object.price)/float(self.object.area)

        # Get related properties (exclude the current property)
        related_properties = Property.objects.filter(is_available=True).exclude(id=self.object.id)#.order_by('-created_at')[:6]

        for property in related_properties:
            # Get main image for each related property
            main_image = property.images.filter(is_main=True).first()
            if not main_image:
                main_image = property.images.first()
            property.main_image = main_image.image.url if main_image else None

        context['related_properties'] = related_properties  # Add related properties to context

        return context

    def post(self, request, *args, **kwargs):
        return redirect('HomeBless:property-detail', pk=self.get_object().pk)