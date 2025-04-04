from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from ..models import Property, PropertyImage

class HomePage(TemplateView):
    template_name = 'homepage.html'
    LOCATIONS = [
        ('ladproa', 'ลาดพร้าว'),
        ('thonglo', 'ทองหล่อ'),
        ('silom', 'สีลม'),
        ('phakanong', 'พระโขนง'),
        ('wipawadee', 'วิภาวดี'),
        ('sukumvit', 'สุขุมวิท'),
        ('asok', 'อโศก'),
        ('aonuch', 'อ่อนนุช'),
    ]

    def get_main_images(self, properties):
        """Return a list of properties with their main images."""
        return [
            {
                'property': prop,
                'main_image': PropertyImage.objects.filter(property=prop, is_main=True).first() or
                              PropertyImage.objects.filter(property=prop).first()
            }
            for prop in properties
        ]

    def get(self, request, *args, **kwargs):
        context = {}

        for key, location_name in self.LOCATIONS:
            properties = Property.objects.filter(location__icontains=location_name).order_by('-created_at')[:3]
            context[key] = self.get_main_images(properties)

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        return redirect('HomeBless:homepage')
