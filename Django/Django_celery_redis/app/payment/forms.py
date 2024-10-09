from django import forms

from .models import ShippingAdress


class ShippingAdressForm(forms.ModelForm):
    class Meta:
        model = ShippingAdress
        fields = [
            "full_name",
            "email",
            "street_adress",
            "apartment_adress",
            "city",
            "country",
            "zip",
        ]
        exclude = ["user"]

