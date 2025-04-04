from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from ..models import Property

@require_POST
def edit_property(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    property.title = request.POST.get('title')
    property.price = request.POST.get('price')
    property.description = request.POST.get('description')
    property.is_available = request.POST.get('is_available')
    property.line_id = request.POST.get('line_id')
    property.phone_number = request.POST.get('phone_number')
    property.contact_email = request.POST.get('contact_email')

    property.save()
    return redirect('HomeBless:manage')
