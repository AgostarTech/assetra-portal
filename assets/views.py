
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    AssetForm,
    AssetDocumentForm,
    VehicleForm,
    LandForm,
    HouseForm,
    StockForm,
    GovernmentBondForm,
)
from .models import Asset, AssetDocument


# ============================================================
# ASSET CATEGORY CONFIGURATION
# ============================================================

CATEGORY_FORMS = {
    Asset.CategoryChoices.VEHICLE: VehicleForm,
    Asset.CategoryChoices.LAND: LandForm,
    Asset.CategoryChoices.HOUSE: HouseForm,
    Asset.CategoryChoices.STOCK: StockForm,
    Asset.CategoryChoices.BOND: GovernmentBondForm,
}

CATEGORY_DETAILS = {
    Asset.CategoryChoices.VEHICLE: "vehicle_details",
    Asset.CategoryChoices.LAND: "land_details",
    Asset.CategoryChoices.HOUSE: "house_details",
    Asset.CategoryChoices.STOCK: "stock_details",
    Asset.CategoryChoices.BOND: "bond_details",
}

CATEGORY_LABELS = {
    Asset.CategoryChoices.VEHICLE: "Vehicles",
    Asset.CategoryChoices.LAND: "Land",
    Asset.CategoryChoices.HOUSE: "Houses",
    Asset.CategoryChoices.STOCK: "Stocks",
    Asset.CategoryChoices.BOND: "Government Bonds",
}

# Sidebar query parameter -> actual Django category value.
CATEGORY_ALIASES = {
    "vehicle": Asset.CategoryChoices.VEHICLE,
    "vehicles": Asset.CategoryChoices.VEHICLE,
    "land": Asset.CategoryChoices.LAND,
    "house": Asset.CategoryChoices.HOUSE,
    "houses": Asset.CategoryChoices.HOUSE,
    "stock": Asset.CategoryChoices.STOCK,
    "stocks": Asset.CategoryChoices.STOCK,
    "bond": Asset.CategoryChoices.BOND,
    "bonds": Asset.CategoryChoices.BOND,
    "government-bond": Asset.CategoryChoices.BOND,
    "government_bond": Asset.CategoryChoices.BOND,
    "government-bonds": Asset.CategoryChoices.BOND,
    "government_bonds": Asset.CategoryChoices.BOND,
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def _get_asset_detail(asset):
    """Return the asset's category-specific details if available."""
    relation_name = CATEGORY_DETAILS.get(asset.category)

    if not relation_name:
        return None

    try:
        return getattr(asset, relation_name)
    except ObjectDoesNotExist:
        return None


def _save_asset_document(document_form, asset, user):
    """Save a supporting document and associate it with its owner and asset."""
    document = document_form.save(commit=False)
    document.asset = asset
    document.uploaded_by = user
    document.save()
    return document


def _get_document_form(request):
    """Build a document form from the current request."""
    if request.method == "POST":
        return AssetDocumentForm(request.POST, request.FILES)

    return AssetDocumentForm()


# ============================================================
# ASSET LIST AND CATEGORY FILTERING
# ============================================================

@login_required
def asset_list(request):
    """List only the logged-in user's active assets."""

    assets = Asset.objects.filter(
        owner=request.user,
        status=Asset.StatusChoices.ACTIVE,
    )

    selected_category = request.GET.get("category", "").strip().lower()
    category = CATEGORY_ALIASES.get(selected_category)

    if selected_category and category is None:
        messages.warning(request, "The selected asset category is invalid.")
        assets = assets.none()

    elif category is not None:
        assets = assets.filter(category=category)

    assets = assets.order_by("-created_at")

    context = {
        "assets": assets,
        "asset_count": assets.count(),
        "selected_category": category,
        "selected_category_label": CATEGORY_LABELS.get(category, "All My Assets"),
        "category_labels": CATEGORY_LABELS,
    }

    return render(request, "assets/asset_list.html", context)


# ============================================================
# SUPPORTING DOCUMENTS
# ============================================================

@login_required
def asset_documents(request):
    """
    Display supporting documents belonging only to the logged-in user's
    assets. The asset ownership filter is applied through the relationship.
    """

    documents = (
        AssetDocument.objects.filter(asset__owner=request.user)
        .select_related("asset", "uploaded_by")
        .order_by("-uploaded_at")
    )

    context = {
        "documents": documents,
        "document_count": documents.count(),
    }

    return render(
        request,
        "assets/asset_documents.html",
        context,
    )


# ============================================================
# GENERIC ASSET CREATION
# ============================================================

@login_required
def create_asset_generic(request, specific_form_class, category, title):
    """Create an asset, its category details, and an optional document."""

    if request.method == "POST":
        asset_form = AssetForm(request.POST)
        specific_form = specific_form_class(request.POST)
        document_form = _get_document_form(request)

        asset_valid = asset_form.is_valid()
        specific_valid = specific_form.is_valid()
        document_valid = document_form.is_valid()

        if asset_valid and specific_valid and document_valid:
            try:
                with transaction.atomic():
                    asset = asset_form.save(commit=False)
                    asset.owner = request.user
                    asset.category = category
                    asset.save()

                    specific = specific_form.save(commit=False)
                    specific.asset = asset
                    specific.save()

                    if document_form.cleaned_data.get("file"):
                        _save_asset_document(
                            document_form,
                            asset,
                            request.user,
                        )

            except Exception:
                messages.error(
                    request,
                    "The asset could not be saved. Check the form and try again.",
                )
            else:
                messages.success(request, f"{title} saved successfully.")
                return redirect("assets:asset_list")

        else:
            messages.error(
                request,
                "Please correct the errors in the form and try again.",
            )

    else:
        asset_form = AssetForm()
        specific_form = specific_form_class()
        document_form = AssetDocumentForm()

    context = {
        "asset_form": asset_form,
        "specific_form": specific_form,
        "document_form": document_form,
        "title": title,
        "category": category,
    }

    return render(request, "assets/asset_form.html", context)


# ============================================================
# CATEGORY-SPECIFIC CREATION VIEWS
# ============================================================

@login_required
def create_vehicle(request):
    return create_asset_generic(
        request,
        VehicleForm,
        Asset.CategoryChoices.VEHICLE,
        "Add New Vehicle",
    )


@login_required
def create_land(request):
    return create_asset_generic(
        request,
        LandForm,
        Asset.CategoryChoices.LAND,
        "Add New Land",
    )


@login_required
def create_house(request):
    return create_asset_generic(
        request,
        HouseForm,
        Asset.CategoryChoices.HOUSE,
        "Add New House",
    )


@login_required
def create_stock(request):
    return create_asset_generic(
        request,
        StockForm,
        Asset.CategoryChoices.STOCK,
        "Add New Stock",
    )


@login_required
def create_bond(request):
    return create_asset_generic(
        request,
        GovernmentBondForm,
        Asset.CategoryChoices.BOND,
        "Add Government Bond",
    )


# ============================================================
# ASSET UPDATE
# ============================================================

@login_required
def asset_update(request, asset_id):
    """Update an asset owned by the current user and optionally add a document."""

    asset = get_object_or_404(
        Asset,
        pk=asset_id,
        owner=request.user,
    )

    specific_form_class = CATEGORY_FORMS.get(asset.category)

    if specific_form_class is None:
        messages.error(request, "This asset category cannot be edited.")
        return redirect("assets:asset_list")

    specific_instance = _get_asset_detail(asset)

    if request.method == "POST":
        asset_form = AssetForm(request.POST, instance=asset)
        specific_form = specific_form_class(
            request.POST,
            instance=specific_instance,
        )
        document_form = _get_document_form(request)

        asset_valid = asset_form.is_valid()
        specific_valid = specific_form.is_valid()
        document_valid = document_form.is_valid()

        if asset_valid and specific_valid and document_valid:
            try:
                with transaction.atomic():
                    updated_asset = asset_form.save(commit=False)

                    # Never accept a different owner or category from a form.
                    updated_asset.owner = request.user
                    updated_asset.category = asset.category
                    updated_asset.save()

                    specific = specific_form.save(commit=False)
                    specific.asset = updated_asset
                    specific.save()

                    if document_form.cleaned_data.get("file"):
                        _save_asset_document(
                            document_form,
                            updated_asset,
                            request.user,
                        )

            except Exception:
                messages.error(
                    request,
                    "The asset could not be updated. Check the form and try again.",
                )
            else:
                messages.success(request, "Asset updated successfully.")
                return redirect("assets:asset_list")

        else:
            messages.error(
                request,
                "Please correct the errors in the form and try again.",
            )

    else:
        asset_form = AssetForm(instance=asset)
        specific_form = specific_form_class(instance=specific_instance)
        document_form = AssetDocumentForm()

    context = {
        "asset_form": asset_form,
        "specific_form": specific_form,
        "document_form": document_form,
        "title": f"Edit Asset: {asset.name}",
        "asset": asset,
        "category": asset.category,
    }

    return render(request, "assets/asset_form.html", context)
