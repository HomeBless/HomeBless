from django.shortcuts import render, redirect
from django.views.generic import TemplateView


class Wishlist(TemplateView):
    template_name = 'wishlist.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return redirect('HomeBless:wishlist')
