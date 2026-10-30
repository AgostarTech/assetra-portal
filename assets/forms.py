
from django import forms

from .models import (
    Asset,
    AssetDocument,
    Vehicle,
    Land,
    House,
    Stock,
    GovernmentBond,
)


# ============================================================
# SHARED FORM STYLING
# ============================================================

ASSET_FIELD_STYLE = (
    "width: 100%; "
    "padding: 8px; "
    "margin-top: 5px; "
    "margin-bottom: 15px; "
    "border: 1px solid #ccc; "
    "border-radius: 4px; "
    "box-sizing: border-box;"
)


def apply_form_styling(form):
    """Apply consistent styling to all fields in a form."""
    for field in form.fields.values():
        field.widget.attrs.update({
            "style": ASSET_FIELD_STYLE,
        })


# ============================================================
# MAIN ASSET FORM
# ============================================================

class AssetForm(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_form_styling(self)


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_form_styling(self)


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_form_styling(self)


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_form_styling(self)


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_form_styling(self)


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_form_styling(self)


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
                    "placeholder": (
                        "e.g. Vehicle registration certificate"
                    ),
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

        apply_form_styling(self)

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
