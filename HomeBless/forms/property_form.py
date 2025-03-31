from django import forms
from django.core.exceptions import ValidationError
from ..models import (
    Property, PropertyType, HomeFeature,
    PropertyCondition, View as PropertyView, Warranty
)

class SellForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'property_type', 'transaction_type',
            'price', 'location', 'latitude', 'longitude',
            'bedrooms', 'bathrooms', 'floors', 'garages', 'area', 'construct_year',
            'decoration', 'flooring', 'wall_type', 'ceiling_type',
            'home_features', 'conditions', 'views', 'warranties',
        ]

        widgets = {
            'transaction_type': forms.RadioSelect,
            'property_type': forms.RadioSelect,
            'decoration': forms.CheckboxSelectMultiple,
            'flooring': forms.CheckboxSelectMultiple,
            'wall_type': forms.CheckboxSelectMultiple,
            'ceiling_type': forms.CheckboxSelectMultiple,
            'home_features': forms.CheckboxSelectMultiple,
            'conditions': forms.CheckboxSelectMultiple,
            'views': forms.CheckboxSelectMultiple,
            'warranties': forms.CheckboxSelectMultiple,
        }

    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get('title')
        price = cleaned_data.get('price')
        area = cleaned_data.get('area')
        location = cleaned_data.get('location')

        if not title:
            self.add_error('title', 'กรุณาระบุหัวข้อประกาศ')

        if price is not None and price <= 0:
            self.add_error('price', 'ราคาต้องมากกว่า 0')

        if area is not None and area <= 0:
            self.add_error('area', 'พื้นที่ต้องมากกว่า 0')

        if not location:
            self.add_error('location', 'กรุณาระบุทำเลที่ตั้ง')

        return cleaned_data
