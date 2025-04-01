from django.shortcuts import render, redirect
from django.views.generic import TemplateView


class PropertyManage(TemplateView):
    template_name = 'property-manage.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return redirect('HomeBless:manage')
