from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from .models import Property, PropertyImage
from django.db.models import Q
from django.core.paginator import Paginator


# Create your views here.
class PropertyListing(ListView):
    model = Property
    template_name = 'property-listing.html'
    context_object_name = 'properties'
    paginate_by = 10  # Add pagination

    def get_queryset(self):
        queryset = Property.objects.filter(is_available=True)
        
        # Get all filter parameters from request
        params = self.request.GET
        
        # Search query (q parameter)
        search_query = params.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(location__icontains=search_query)
            )
        
        # Property type filter
        property_type = params.get('property_type')
        if property_type:
            queryset = queryset.filter(property_type=property_type)
        
        # Transaction type (buy/rent)
        transaction_type = params.get('transaction_type')
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        
        # Price range
        min_price = params.get('min_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        
        max_price = params.get('max_price')
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Bedrooms
        bedrooms = params.get('bedrooms')
        if bedrooms:
            queryset = queryset.filter(bedrooms=bedrooms)
        
        # Bathrooms
        bathrooms = params.get('bathrooms')
        if bathrooms:
            queryset = queryset.filter(bathrooms=bathrooms)
        
        # Area
        min_area = params.get('min_area')
        if min_area:
            queryset = queryset.filter(area__gte=min_area)
        
        max_area = params.get('max_area')
        if max_area:
            queryset = queryset.filter(area__lte=max_area)
        
        # Order by newest first
        queryset = queryset.order_by('-created_at')
        
        # Add main image to each property
        for property in queryset:
            main_image = property.images.filter(is_main=True).first()
            if not main_image:
                main_image = property.images.first()
            property.main_image = main_image.image.url if main_image else None
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add current filters to context
        context['current_filters'] = {
            'q': self.request.GET.get('q', ''),
            'property_type': self.request.GET.get('property_type', ''),
            'transaction_type': self.request.GET.get('transaction_type', ''),
            'min_price': self.request.GET.get('min_price', ''),
            'max_price': self.request.GET.get('max_price', ''),
            'bedrooms': self.request.GET.get('bedrooms', ''),
            'bathrooms': self.request.GET.get('bathrooms', ''),
            'min_area': self.request.GET.get('min_area', ''),
            'max_area': self.request.GET.get('max_area', ''),
        }
        # Add choices for dropdowns
        context['property_type_choices'] = Property.PROPERTY_TYPE_CHOICES
        context['transaction_type_choices'] = Property.SELLING_TYPE_CHOICES
        return context

def property_list(request):
    properties = Property.objects.all()
    return render(request, 'property-listing.html', {'properties': properties})


class HomePage(TemplateView):
    template_name = 'homepage.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return redirect('HomeBless:homepage')


class Compare(TemplateView):
    template_name = 'compare.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return redirect('HomeBless:compare')


class PropertyDetail(DetailView):
    model = Property
    template_name = 'property-detail.html'
    context_object_name = 'property'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the main image (if marked) or fallback to the first available image
        main_image = self.object.images.filter(is_main=True).first()
        if not main_image:
            main_image = self.object.images.first()

        # Get extra images excluding the main image
        extra_images = self.object.images.exclude(id=main_image.id) if main_image else self.object.images.all()

        # Add attributes to the property object
        self.object.main_image = main_image.image.url if main_image else None
        self.object.extra_images = extra_images
        self.object.price_per_area = float(self.object.price)/float(self.object.area)

        # Get related properties (exclude the current property)
        related_properties = Property.objects.filter(is_available=True).exclude(id=self.object.id).order_by('-created_at')[:6]

        for property in related_properties:
            # Get main image for each related property
            main_image = property.images.filter(is_main=True).first()
            if not main_image:
                main_image = property.images.first()
            property.main_image = main_image.image.url if main_image else None

        context['related_properties'] = related_properties  # Add related properties to context

        return context

    def post(self, request, *args, **kwargs):
        return redirect('HomeBless:property-detail', pk=self.get_object().pk)


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

