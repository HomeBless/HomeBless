from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from ..forms import PropertyForm
from ..models import PropertyImage


@method_decorator(login_required, name='dispatch')
class Sell(TemplateView):
    template_name = 'sell.html'

    def get(self, request, *args, **kwargs):
        form = PropertyForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = PropertyForm(request.POST, request.FILES)

        if form.is_valid():
            property_obj = form.save(commit=False)

            if not request.user.is_authenticated:
                return render(request, self.template_name, {
                    'form': form,
                    'error': "You must be logged in to list a property."
                })

            property_obj.user = request.user
            property_obj.save()
            form.save_m2m()

            image_files = request.FILES.getlist('images[]')
            cover_index = int(request.POST.get('cover_image_index', 0))

            print("FILES:", request.FILES)
            print("IMAGES[]:", request.FILES.getlist("images[]"))
            print("NEW PROPERTY ID:", property_obj.id)
            for i, image_file in enumerate(image_files):
                print(i)
                print(image_file)
                prop_img = PropertyImage(
                    property=property_obj,
                    is_main=(i == cover_index)
                )
                prop_img.image.save(image_file.name, image_file)
                prop_img.save()
                print(f"Saved image: {prop_img.image.url}")

            return redirect('HomeBless:sell')
        print(form.errors)
        return render(request, self.template_name, {'form': form})
