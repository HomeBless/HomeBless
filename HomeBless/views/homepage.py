from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from ..models import Property, PropertyImage


class HomePage(TemplateView):
    template_name = 'homepage.html'

    def get_main_images(self, properties):
        """Return a list of tuples (property, main_image)"""
        return [
            {
                'property': prop,
                'main_image': PropertyImage.objects.filter(property=prop, is_main=True).first()
                              or PropertyImage.objects.filter(property=prop).first()
            }
            for prop in properties
        ]

    def get(self, request, *args, **kwargs):
        locations = {
            'ladproa': 'ลาดพร้าว',
            'thonglo': 'ทองหล่อ',
            'silom': 'สีลม',
            'phakanong': 'พระโขนง',
            'wipawadee': 'วิภาวดี',
            'sukumvit': 'สุขุมวิท',
            'asok': 'อโศก',
            'aonuch': 'อ่อนนุช',
        }

        context = {}

        for key, name in locations.items():
            props = Property.objects.filter(location__icontains=name).order_by('-created_at')[:3]
            context[key] = self.get_main_images(props)

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        return redirect('HomeBless:homepage')
