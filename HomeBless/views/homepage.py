import logging
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from ..models import Property

logger = logging.getLogger(__name__)


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

    def get(self, request, *args, **kwargs):
        context = {}
        for key, location in self.LOCATIONS:
            queryset = Property.objects.filter(location__icontains=location).order_by('-created_at')[:3]
            context[key] = queryset
            logger.info(f"Loaded {queryset.count()} properties for {location}")
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        return redirect('HomeBless:homepage')
