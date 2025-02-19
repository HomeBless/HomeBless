from django.urls import path
from . import views

app_name = "HomeBless"

urlpatterns = [
    path('', views.HomePage.as_view(), name='homepage'),
    path('property-listing/', views.PropertyListing.as_view(), name='property-listing'),
    path('compare/', views.Compare.as_view(), name='compare'),
    path('property-detail/<int:pk>/', views.PropertyDetail.as_view(), name='property-detail'),
]
