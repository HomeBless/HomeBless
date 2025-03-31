from django.urls import path
from .views import *
app_name = "HomeBless"

urlpatterns = [
    path('', HomePage.as_view(), name='homepage'),
    path('property-listing/', PropertyListing.as_view(), name='property-listing'),
    path('compare/', Compare.as_view(), name='compare'),
    path('property-detail/<int:pk>/', PropertyDetail.as_view(), name='property-detail'),
]
