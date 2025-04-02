from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Property



class PropertyManage(LoginRequiredMixin, TemplateView):
    template_name = 'property-manage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['properties'] = Property.objects.filter(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        property_id = request.POST.get('delete_property_id')
        if property_id:
            property_instance = get_object_or_404(Property, id=property_id, user=request.user)
            property_instance.delete()
        return redirect('HomeBless:manage')