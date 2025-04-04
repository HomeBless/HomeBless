from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from mysite import settings
from ..forms import PropertyForm
from django.contrib.auth.models import User


@method_decorator(login_required, name='dispatch')
class Sell(TemplateView):
    template_name = 'sell.html'

    def get(self, request, *args, **kwargs):
        form = PropertyForm()
        return render(request, self.template_name, {
            'form': form,
            'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
        })


    def post(self, request, *args, **kwargs):
        form = PropertyForm(request.POST)

        if form.is_valid():
            property_obj = form.save(commit=False)

            if not request.user.is_authenticated:
                return render(request, self.template_name, {
                    'form': form,
                    'error': "You must be logged in to list a property."
                })

            property_obj.latitude = request.POST.get('latitude')
            property_obj.longitude = request.POST.get('longitude')
            property_obj.user = request.user
            property_obj.save()
            form.save_m2m()

            return redirect('HomeBless:sell')
        print(form.errors)
        return render(request, self.template_name, {
            'form': form,
            'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
        })
