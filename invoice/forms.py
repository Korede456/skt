from django import forms
from .models import Item, Invoice

# forms.py

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['description', 'unit_price', 'quantity']


class InvoiceForm(forms.ModelForm):
    # Billed To Fields
    billed_to_1 = forms.CharField(max_length=255, required=True, label="Company Name")
    billed_to_2 = forms.CharField(max_length=255, required=True, label="Street Address")
    billed_to_3 = forms.CharField(max_length=255, required=True, label="City, State and Country")

    # Payment Info Fields
    payment_info_1 = forms.CharField(max_length=255, required=True, label="Bank")
    payment_info_2 = forms.CharField(max_length=255, required=True, label="Account Name")
    payment_info_3 = forms.CharField(max_length=255, required=True, label="Account No")
    payment_info_4 = forms.CharField(max_length=255, required=True, label="Swift Code")
    payment_info_5 = forms.CharField(max_length=255, required=True, label="Sort Code")
    payment_info_6 = forms.CharField(max_length=255, required=True, label="Tin")

    class Meta:
        model = Invoice
        fields = []  # No direct model fields used here

    def clean(self):
        cleaned_data = super().clean()
        
        # Convert form fields to JSON format
        cleaned_data["billed_to"] = {
            "line_1": cleaned_data.get("billed_to_1", ""),
            "line_2": cleaned_data.get("billed_to_2", ""),
            "line_3": cleaned_data.get("billed_to_3", ""),
        }

        cleaned_data["payment_info"] = {
            "detail_1": cleaned_data.get("payment_info_1", ""),
            "detail_2": cleaned_data.get("payment_info_2", ""),
            "detail_3": cleaned_data.get("payment_info_3", ""),
            "detail_4": cleaned_data.get("payment_info_4", ""),
            "detail_5": cleaned_data.get("payment_info_5", ""),
            "detail_6": cleaned_data.get("payment_info_6", ""),
        }

        return cleaned_data
