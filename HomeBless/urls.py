from django.urls import path
from .views import *
app_name = "HomeBless"

urlpatterns = [
    path('', HomePage.as_view(), name='homepage'),
    path('property-listing/', PropertyListing.as_view(), name='property-listing'),
    path('compare/', Compare.as_view(), name='compare'),
    path('property-detail/<int:pk>/', PropertyDetail.as_view(), name='property-detail'),
    path('sell/', Sell.as_view(), name='sell'),
    path('wishlist/', Wishlist.as_view(), name='wishlist'),
]
