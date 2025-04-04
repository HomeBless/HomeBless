from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from ..models import Property


class HomePage(TemplateView):
    template_name = 'homepage.html'

    def get(self, request, *args, **kwargs):
        """Render the homepage template"""
        ladproa = Property.objects.filter(location__icontains='ลาดพร้าว').order_by(
            '-created_at'
        )[:3]
        thonglo = Property.objects.filter(location__icontains='ทองหล่อ').order_by(
            '-created_at'
        )[:3]
        silom = Property.objects.filter(location__icontains='สีลม').order_by(
            '-created_at'
        )[:3]
        phakanong = Property.objects.filter(location__icontains='พระโขนง').order_by(
            '-created_at'
        )[:3]
        wipawadee = Property.objects.filter(location__icontains='วิภาวดี').order_by(
            '-created_at'
        )[:3]
        sukumvit = Property.objects.filter(location__icontains='สุขุมวิท').order_by(
            '-created_at'
        )[:3]
        asok = Property.objects.filter(location__icontains='อโศก').order_by(
            '-created_at'
        )[:3]
        aonuch = Property.objects.filter(location__icontains='อ่อนนุช').order_by(
            '-created_at'
        )[:3]

        context = {
            'ladproa': ladproa,
            'thonglo': thonglo,
            'silom': silom,
            'phakanong': phakanong,
            'wipawadee': wipawadee,
            'sukumvit': sukumvit,
            'asok': asok,
            'aonuch': aonuch,
        }

        print(
            "ladproa:",
            ladproa,
            "thonglo:",
            thonglo,
            "silom:",
            silom,
            "phakanong:",
            phakanong,
            "wipawadee:",
            wipawadee,
            "sukumvit:",
            sukumvit,
            "asok:",
            asok,
            "aonuch:",
            aonuch,
        )

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        return redirect('HomeBless:homepage')
