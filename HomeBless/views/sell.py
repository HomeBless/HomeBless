import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from mysite import settings

from ..forms import PropertyForm
from ..models import PropertyImage

logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class Sell(TemplateView):
    template_name = 'sell.html'

    def get(self, request, *args, **kwargs):
        form = PropertyForm()
        return render(
            request,
            self.template_name,
            {'form': form, 'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY},
        )

    def post(self, request, *args, **kwargs):
        form = PropertyForm(request.POST, request.FILES)

        if form.is_valid():
            property_obj = form.save(commit=False)

            if not request.user.is_authenticated:
                logger.warning("Unauthenticated user tried to post property.")
                return render(
                    request,
                    self.template_name,
                    {
                        'form': form,
                        'error': "You must be logged in to list a property.",
                    },
                )

            property_obj.latitude = request.POST.get('latitude')
            property_obj.longitude = request.POST.get('longitude')
            property_obj.user = request.user
            property_obj.save()
            form.save_m2m()

            image_files = request.FILES.getlist('images[]')
            cover_index = int(request.POST.get('cover_image_index', 0))

            for i, image_file in enumerate(image_files):
                try:
                    prop_img = PropertyImage(
                        property=property_obj, is_main=(i == cover_index)
                    )
                    prop_img.image.save(image_file.name, image_file)
                    prop_img.save()
                    logger.debug(f"Saved image {i}: {prop_img.image.url}")
                except Exception as e:
                    logger.error(f"Error saving image {i}: {e}")

            return redirect('HomeBless:sell')

        logger.error(f"Form invalid: {form.errors}")
        return render(
            request,
            self.template_name,
            {'form': form, 'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY},
        )
