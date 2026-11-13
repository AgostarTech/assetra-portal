from decimal import Decimal, InvalidOperation
from django import forms

from .models import (
    Asset,
    AssetDocument,
    Vehicle,
    Land,
    House,
    Stock,
    GovernmentBond,
    OtherAsset,
)


# ============================================================
# MAIN ASSET FORM
# ============================================================

class AssetForm(forms.ModelForm):
    CURRENCY_CHOICES = [
        ("TZS", "TZS - Tanzanian Shilling"),
        ("KES", "KES - Kenyan Shilling"),
        ("UGX", "UGX - Ugandan Shilling"),
        ("RWF", "RWF - Rwandan Franc"),
        ("BIF", "BIF - Burundian Franc"),
        ("USD", "USD - US Dollar ($)"),
        ("EUR", "EUR - Euro (€)"),
    ]

    currency = forms.ChoiceField(
        choices=CURRENCY_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"})
    )

    # Explicitly defined as CharField so Django doesn't block commas early
    purchase_price = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "0.00"})
    )
    current_estimated_value = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "0.00"})
    )

    class Meta:
        model = Asset
        fields = [
            "name",
            "unique_reference",
            "purchase_price",
            "purchase_date",
            "current_estimated_value",
            "valuation_date",
            "currency",
            "description",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Asset Name"}
            ),
            "unique_reference": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Unique ID or Reference"}
            ),
            "purchase_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "valuation_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "description": forms.Textarea(
                attrs={"rows": 3, "class": "form-control", "placeholder": "Optional description..."}
            ),
        }

    def clean_purchase_price(self):
        data = self.cleaned_data.get("purchase_price")
        if data in [None, ""]:
            return None
        if isinstance(data, str):
            cleaned_str = data.replace(",", "").strip()
            if not cleaned_str:
                return None
            try:
                return Decimal(cleaned_str)
            except InvalidOperation:
                raise forms.ValidationError("Enter a valid number.")
        return data

    def clean_current_estimated_value(self):
        data = self.cleaned_data.get("current_estimated_value")
        if data in [None, ""]:
            return None
        if isinstance(data, str):
            cleaned_str = data.replace(",", "").strip()
            if not cleaned_str:
                return None
            try:
                return Decimal(cleaned_str)
            except InvalidOperation:
                raise forms.ValidationError("Enter a valid number.")
        return data


# ============================================================
# VEHICLE FORM
# ============================================================

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            "registration_number",
            "make",
            "model",
            "year",
        ]
        widgets = {
            "registration_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "e.g., T 123 ABC"}
            ),
            "make": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "e.g., Toyota"}
            ),
            "model": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "e.g., Land Cruiser"}
            ),
            "year": forms.NumberInput(
                attrs={"class": "form-control", "min": "1900", "max": "2030", "placeholder": "YYYY"}
            ),
        }

    def clean_year(self):
        year = self.cleaned_data.get("year")
        if year is not None:
            if year < 1900 or year > 2030:
                raise forms.ValidationError("Please enter a valid manufacturing year between 1900 and 2030.")
        return year


# ============================================================
# LAND FORM
# ============================================================

class LandForm(forms.ModelForm):
    size = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "0.00"})
    )

    class Meta:
        model = Land
        fields = [
            "location",
            "plot_reference",
            "size",
            "measurement_unit",
        ]
        widgets = {
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "plot_reference": forms.TextInput(attrs={"class": "form-control"}),
            "measurement_unit": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., Acres, Sq Meters"})
        }

    def clean_size(self):
        data = self.cleaned_data.get("size")
        if data in [None, ""]:
            return None
        if isinstance(data, str):
            cleaned_str = data.replace(",", "").strip()
            if not cleaned_str:
                return None
            try:
                return Decimal(cleaned_str)
            except InvalidOperation:
                raise forms.ValidationError("Enter a valid number.")
        return data


# ============================================================
# HOUSE FORM
# ============================================================

class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = [
            "location",
            "property_identification",
            "building_information",
        ]

        widgets = {
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "property_identification": forms.TextInput(attrs={"class": "form-control"}),
            "building_information": forms.Textarea(
                attrs={"rows": 3, "class": "form-control"}
            ),
        }


# ============================================================
# STOCK FORM
# ============================================================

class StockForm(forms.ModelForm):
    units = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "0"})
    )

    class Meta:
        model = Stock
        fields = [
            "company",
            "ticker",
            "units",
        ]
        widgets = {
            "company": forms.TextInput(attrs={"class": "form-control"}),
            "ticker": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_units(self):
        data = self.cleaned_data.get("units")
        if data in [None, ""]:
            return None
        if isinstance(data, str):
            cleaned_str = data.replace(",", "").strip()
            if not cleaned_str:
                return None
            try:
                return Decimal(cleaned_str)
            except InvalidOperation:
                raise forms.ValidationError("Enter a valid number.")
        return data


# ============================================================
# GOVERNMENT BOND FORM
# ============================================================

class GovernmentBondForm(forms.ModelForm):
    face_value = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "0.00"})
    )
    coupon_rate = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "0.00"})
    )

    class Meta:
        model = GovernmentBond
        fields = [
            "issuer",
            "face_value",
            "coupon_rate",
            "maturity_date",
        ]

        widgets = {
            "issuer": forms.TextInput(attrs={"class": "form-control"}),
            "maturity_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
        }

    def clean_face_value(self):
        data = self.cleaned_data.get("face_value")
        if data in [None, ""]:
            return None
        if isinstance(data, str):
            cleaned_str = data.replace(",", "").strip()
            if not cleaned_str:
                return None
            try:
                return Decimal(cleaned_str)
            except InvalidOperation:
                raise forms.ValidationError("Enter a valid number.")
        return data

    def clean_coupon_rate(self):
        data = self.cleaned_data.get("coupon_rate")
        if data in [None, ""]:
            return None
        if isinstance(data, str):
            cleaned_str = data.replace(",", "").strip()
            if not cleaned_str:
                return None
            try:
                return Decimal(cleaned_str)
            except InvalidOperation:
                raise forms.ValidationError("Enter a valid number.")
        return data


# ============================================================
# OTHER ASSET FORM
# ============================================================

class OtherAssetForm(forms.ModelForm):
    class Meta:
        model = OtherAsset
        fields = [
            "asset_sub_type",
            "serial_number_or_identifier",
        ]
        widgets = {
            "asset_sub_type": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g., Artwork, Machinery, Jewelry",
                }
            ),
            "serial_number_or_identifier": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Serial number or unique ID (optional)",
                }
            ),
        }
        labels = {
            "asset_sub_type": "Asset Type / Category",
            "serial_number_or_identifier": "Serial Number / Identifier",
        }


# ============================================================
# ASSET SUPPORTING DOCUMENT FORM
# ============================================================

class AssetDocumentForm(forms.ModelForm):
    class Meta:
        model = AssetDocument
        fields = [
            "title",
            "document_type",
            "file",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Vehicle registration certificate",
                }
            ),
            "document_type": forms.Select(
                attrs={"class": "form-select"}
            ),
            "file": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": ".pdf,.jpg,.jpeg,.png",
                }
            ),
        }

        help_texts = {
            "file": (
                "Accepted formats: PDF, JPG, JPEG, PNG. "
                "Maximum file size: 10 MB."
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["file"].required = False
        self.fields["title"].required = False
        self.fields["document_type"].required = False

    def clean(self):
        cleaned_data = super().clean()

        uploaded_file = cleaned_data.get("file")
        title = cleaned_data.get("title")
        document_type = cleaned_data.get("document_type")

        if uploaded_file:
            if not title:
                self.add_error(
                    "title",
                    "Enter a title for the uploaded document.",
                )

            if not document_type:
                self.add_error(
                    "document_type",
                    "Select a document type.",
                )

        return cleaned_data