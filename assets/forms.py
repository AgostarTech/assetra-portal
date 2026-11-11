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
    # East African Currencies + USD and EUR Dropdown Choices
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
            "purchase_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "valuation_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "description": forms.Textarea(
                attrs={"rows": 3}
            ),
        }


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


# ============================================================
# LAND FORM
# ============================================================

class LandForm(forms.ModelForm):
    class Meta:
        model = Land
        fields = [
            "location",
            "plot_reference",
            "size",
            "measurement_unit",
        ]


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
            "building_information": forms.Textarea(
                attrs={"rows": 3}
            ),
        }


# ============================================================
# STOCK FORM
# ============================================================

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = [
            "company",
            "ticker",
            "units",
        ]


# ============================================================
# GOVERNMENT BOND FORM
# ============================================================

class GovernmentBondForm(forms.ModelForm):
    class Meta:
        model = GovernmentBond
        fields = [
            "issuer",
            "face_value",
            "coupon_rate",
            "maturity_date",
        ]

        widgets = {
            "maturity_date": forms.DateInput(
                attrs={"type": "date"}
            ),
        }


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
                    "placeholder": "e.g., Artwork, Machinery, Jewelry",
                }
            ),
            "serial_number_or_identifier": forms.TextInput(
                attrs={
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
                    "placeholder": "e.g. Vehicle registration certificate",
                }
            ),
            "file": forms.ClearableFileInput(
                attrs={
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

        # A document is optional when creating or editing an asset.
        self.fields["file"].required = False

        # Title and document type are required only when a file is uploaded.
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