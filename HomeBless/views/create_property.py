from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import TemplateView

from ..models import Seller
from ..forms import SellForm

@login_required
class Sell(TemplateView):
    template_name = 'sell.html'

    def get(self, request, *args, **kwargs):
        form = SellForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = SellForm(request.POST, request.FILES)
        if form.is_valid():
            print("Cleaned Data:", form.cleaned_data)
            # Save to DB logic here (if applicable)
            return redirect('HomeBless:sell')
        else:
            print("Form Errors:", form.errors)
        return render(request, self.template_name, {'form': form})

