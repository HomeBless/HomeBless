from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from ..forms import PropertyForm
from ..models import Seller


@method_decorator(login_required, name='dispatch')
class Sell(TemplateView):
    template_name = 'sell.html'

    def get(self, request, *args, **kwargs):
        form = PropertyForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = PropertyForm(request.POST)

        if form.is_valid():
            property_obj = form.save(commit=False)

            try:
                seller = Seller.objects.get(user=request.user)
            except Seller.DoesNotExist:
                return render(request, self.template_name, {
                    'form': form,
                    'error': "You must be registered as a seller to post a property."
                })

            property_obj.seller = seller
            property_obj.save()
            form.save_m2m()

            return redirect('HomeBless:sell')
        print(form.errors)
        return render(request, self.template_name, {'form': form})
