from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from ..models import Property


@require_POST
def edit_property(request, property_id):
    prop = get_object_or_404(Property, id=property_id)
    fields = ['title',
              'price',
              'description',
              'is_available',
              'line_id',
              'phone_number',
              'contact_email'
              ]

    for field in fields:
        setattr(prop, field, request.POST.get(field))
    prop.save()
    return redirect('HomeBless:manage')
