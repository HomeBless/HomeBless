from django.core.paginator import Paginator
from django.views.generic import ListView
from django.db.models import Q
from ..models import Property, PropertyType, Wishlist

PROPERTY_PER_PAGE = 9

class PropertyListing(ListView):
    model = Property
    template_name = 'property-listing.html'
    context_object_name = 'properties'
    paginate_by = PROPERTY_PER_PAGE

    def get_filters(self):
        """Helper function to get and parse the filter parameters"""
        return self.request.GET

    @staticmethod
    def filter_by_search(queryset, search_query):
        """Enhanced search across multiple relevant fields"""
        if search_query:
            return queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(location__icontains=search_query)
            )
        return queryset

    @staticmethod
    def filter_by_listing_type(queryset, listing_type):
        """Filter by selling type (buy/rent)"""
        if listing_type == 'sell':
            return queryset.filter(selling_type='buy')
        elif listing_type == 'rent':
            return queryset.filter(selling_type='rent')
        elif listing_type == 'other':
            return queryset.exclude(selling_type__in=['buy', 'rent'])
        return queryset

    @staticmethod
    def filter_by_property_type(queryset, filters):
        """Filter properties by type"""
        if filters.get('property_type'):
            filter_criteria = filters.getlist('property_type')  # list [House, Condo]
            filter_id = PropertyType.objects.filter(name__in=filter_criteria).values_list('id', flat=True)
            queryset = queryset.filter(property_type__in=filter_id)
        return queryset

    @staticmethod
    def filter_by_bedrooms(queryset, filters):
        """Filter properties by number of bedrooms"""
        if filters.get('bedrooms'):
            bedrooms = filters.getlist('bedrooms')
            regular_beds = [int(bed) for bed in bedrooms if bed.isdigit()]
            has_more_than_4 = "more_than_4" in bedrooms

            q_filter = Q()
            if regular_beds:
                q_filter |= Q(bedrooms__in=regular_beds)
            if has_more_than_4:
                q_filter |= Q(bedrooms__gte=5)
            queryset = queryset.filter(q_filter)
        return queryset

    @staticmethod
    def filter_by_bathrooms(queryset, filters):
        """Filter properties by number of bathrooms"""
        if filters.get('bathrooms'):
            bathrooms = filters.getlist('bathrooms')
            regular_baths = [int(bath) for bath in bathrooms if bath.isdigit()]
            has_more_than_5 = "more_than_5" in bathrooms

            q_filter = Q()
            if regular_baths:
                q_filter |= Q(bathrooms__in=regular_baths)
            if has_more_than_5:
                q_filter |= Q(bathrooms__gte=6)
            queryset = queryset.filter(q_filter)
        return queryset

    @staticmethod
    def filter_by_parking(queryset, filters):
        """Filter properties by number of parking spaces"""
        if filters.get('parking'):
            parking = filters.getlist('parking')
            regular_parking = [int(park) for park in parking if park.isdigit()]
            has_more_than_3 = "more_than_4" in parking

            q_filter = Q()
            if regular_parking:
                q_filter |= Q(garages__in=regular_parking)
            if has_more_than_3:
                q_filter |= Q(garages__gte=5)
            queryset = queryset.filter(q_filter)
        return queryset

    @staticmethod
    def filter_by_price(queryset, filters):
        """Filter properties by price range"""
        if filters.get('price_min'):
            queryset = queryset.filter(price__gte=filters.get('price_min'))
        if filters.get('price_max'):
            queryset = queryset.filter(price__lte=filters.get('price_max'))
        return queryset

    @staticmethod
    def filter_by_area(queryset, filters):
        """Filter properties by area range"""
        if filters.get('area_min'):
            queryset = queryset.filter(area__gte=filters.get('area_min'))
        if filters.get('area_max'):
            queryset = queryset.filter(area__lte=filters.get('area_max'))
        return queryset

    def get_queryset(self):
        """Override the get_queryset method to apply filters and sorting"""
        queryset = Property.objects.filter(is_available=True)
        filters = self.get_filters()

        search_query = filters.get('search')
        if search_query:
            queryset = self.filter_by_search(queryset, search_query)

        listing_type = filters.get('listing_type')
        if listing_type:
            queryset = self.filter_by_listing_type(queryset, listing_type)

        queryset = self.filter_by_property_type(queryset, filters)
        queryset = self.filter_by_bedrooms(queryset, filters)
        queryset = self.filter_by_bathrooms(queryset, filters)
        queryset = self.filter_by_parking(queryset, filters)
        queryset = self.filter_by_price(queryset, filters)
        queryset = self.filter_by_area(queryset, filters)

        sort_option = self.request.GET.get('sort', 'latest')

        if sort_option == 'latest':
            queryset = queryset.order_by('-created_at')
        elif sort_option == 'oldest':
            queryset = queryset.order_by('created_at')
        elif sort_option == 'price-asc':
            queryset = queryset.order_by('price')
        elif sort_option == 'price-desc':
            queryset = queryset.order_by('-price')

        return queryset

    def get_context_data(self, **kwargs):
        """Override the get_context_data method to add additional context"""
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            wishlist_properties = Wishlist.objects.filter(
                user=self.request.user
            ).values_list('property_id', flat=True)
            context['wishlist_properties'] = wishlist_properties

        for property in context['object_list']:
            main_image = property.images.filter(is_main=True).first() or property.images.first()
            property.main_image = main_image.image.url if main_image else None

        context.update({
            'current_sort': self.request.GET.get('sort', 'latest'),
            'empty_message': 'ไม่พบคุณสมบัติบ้านที่ตรงตามเกณฑ์ของคุณ',
            'user_is_authenticated': self.request.user.is_authenticated,
            'search_query': self.request.GET.get('search', ''),
            'current_listing_type': self.request.GET.get('listing_type', ''),
        })

        if 'page_obj' not in context:
            paginator = Paginator(self.get_queryset(), self.paginate_by)
            page_number = self.request.GET.get('page')
            context['page_obj'] = paginator.get_page(page_number)

        return context
