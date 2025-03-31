from django.shortcuts import render, redirect
from django.views.generic import TemplateView


# @login_required
class Sell(TemplateView):
    template_name = 'sell.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        print("Form Data Received:", request.POST)

        status = request.POST.get('status')

        if status:
            print(f"Status selected: {status}")
        else:
            print("No status selected")

        return redirect('HomeBless:sell')
