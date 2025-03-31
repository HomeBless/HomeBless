import datetime
from django import forms
from ..models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ['seller']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

    def clean_area(self):
        area = self.cleaned_data.get('area')
        if area is not None and area <= 0:
            raise forms.ValidationError("Area must be greater than zero.")
        return area

    def clean_construct_year(self):
        year = self.cleaned_data.get('construct_year')
        current_year = datetime.datetime.now().year
        if year and (year < 1900 or year > current_year):
            raise forms.ValidationError(f"Construction year must be between 1900 and {current_year}.")
        return year

    def clean(self):
        cleaned_data = super().clean()

        bedrooms = cleaned_data.get('bedrooms')
        bathrooms = cleaned_data.get('bathrooms')

        if bedrooms is not None and bedrooms < 0:
            self.add_error('bedrooms', "Bedrooms cannot be negative.")

        if bathrooms is not None and bathrooms < 0:
            self.add_error('bathrooms', "Bathrooms cannot be negative.")