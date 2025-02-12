from django.urls import path
from . import views

app_name = "HomeBless"

urlpatterns = [
    path('', views.PropertyListing.as_view(), name='property-listing'),
]
