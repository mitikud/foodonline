from django import forms

from accounts.validator import allow_only_image_validator
from .models import Vendor

class VendorForm(forms.ModelForm):
    # vendor_license = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}))
    vendor_license = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_image_validator])
    class Meta:
        model = Vendor
        fields = ['vendor_name','vendor_license']