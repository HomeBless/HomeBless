from django import forms
from django.core.exceptions import ValidationError
from ..models import (
    Property, PropertyType, HomeFeature,
    ProjectAmenity, PropertyCondition, View as PropertyView, Warranty
)

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'property_type', 'transaction_type',
            'price', 'location', 'latitude', 'longitude', 'bedrooms',
            'bathrooms', 'floors', 'garages', 'area', 'construct_year',
            'decoration', 'flooring', 'wall_type', 'ceiling_type',
            'home_features', 'project_amenities', 'conditions', 'views', 'warranties',
            'electrical_system', 'air_conditioning', 'hot_cold_water',
            'safety_circuit_breaker', 'backup_power', 'drainage_system'
        ]

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'transaction_type': forms.Select(choices=Property.SELLING_TYPE_CHOICES),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'latitude': forms.NumberInput(attrs={'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'step': '0.000001'}),
            'bedrooms': forms.NumberInput(attrs={'min': 0}),
            'bathrooms': forms.NumberInput(attrs={'min': 0}),
            'floors': forms.NumberInput(attrs={'min': 0}),
            'garages': forms.NumberInput(attrs={'min': 0}),
            'area': forms.NumberInput(attrs={'min': 0}),
            'construct_year': forms.NumberInput(attrs={'min': 1900, 'max': 2100}),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None or price <= 0:
            raise ValidationError("Price must be greater than 0.")
        return price

    def clean_area(self):
        area = self.cleaned_data.get('area')
        if area is None or area <= 0:
            raise ValidationError("Area must be a positive number.")
        return area

    def clean_bedrooms(self):
        bedrooms = self.cleaned_data.get('bedrooms')
        if bedrooms is not None and bedrooms < 0:
            raise ValidationError("Bedrooms cannot be negative.")
        return bedrooms

    def clean_bathrooms(self):
        bathrooms = self.cleaned_data.get('bathrooms')
        if bathrooms is not None and bathrooms < 0:
            raise ValidationError("Bathrooms cannot be negative.")
        return bathrooms

    def clean_garages(self):
        garages = self.cleaned_data.get('garages')
        if garages is not None and garages < 0:
            raise ValidationError("Garages cannot be negative.")
        return garages

    def clean_construct_year(self):
        construct_year = self.cleaned_data.get('construct_year')
        if construct_year is not None and (construct_year < 1900 or construct_year > 2100):
            raise ValidationError("Construction year must be between 1900 and 2100.")
        return construct_year

    def clean_property_type(self):
        property_type = self.cleaned_data.get('property_type')
        if property_type is not None and not PropertyType.objects.filter(id=property_type.id).exists():
            raise ValidationError("Invalid property type.")
        return property_type

    def save(self, seller, commit=True):
        """
        Custom save method to associate the property with a seller and handle ManyToMany fields.
        """
        property_instance = super().save(commit=False)
        property_instance.seller = seller  # Assign the seller

        if commit:
            property_instance.save()  # Save the main Property instance

            # Handle ManyToMany relationships
            self.save_m2m()

        return property_instance
