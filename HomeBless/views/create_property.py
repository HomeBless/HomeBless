from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from ..models import Seller
from ..forms import PropertyForm

@login_required
def create_property_view(request):
    if request.method == "POST":
        form = PropertyForm(request.POST)

        if form.is_valid():
            try:
                seller = Seller.objects.get(user=request.user)
                form.save(seller=seller)  # Use the custom save method to associate seller
                return redirect('property_list')  # Redirect to property listing page
            except Seller.DoesNotExist:
                return HttpResponse("Only sellers can create properties", status=403)
        else:
            return render(request, 'create_property.html', {'form': form})  # Return form with errors

    else:
        form = PropertyForm()

    return render(request, 'create_property.html', {'form': form})
