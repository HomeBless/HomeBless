from django.shortcuts import render

from ..models import Property


def property_list(request):
    properties = Property.objects.all()
    return render(request, 'property-listing.html', {'properties': properties})
