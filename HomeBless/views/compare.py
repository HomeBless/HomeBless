from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from ..models.wishlist import Wishlist


class Compare(TemplateView):
    template_name = 'compare.html'

    def get(self, request, *args, **kwargs):
        wishlist_items = Wishlist.objects.filter

        context = {
            'wishlist': wishlist_items,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        return redirect('HomeBless:compare')
