import os
import io
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    AssetForm,
    AssetDocumentForm,
    VehicleForm,
    LandForm,
    HouseForm,
    StockForm,
    GovernmentBondForm,
    OtherAssetForm,
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
    Asset.CategoryChoices.OTHER: OtherAssetForm,
}

CATEGORY_DETAILS = {
    Asset.CategoryChoices.VEHICLE: "vehicle_details",
    Asset.CategoryChoices.LAND: "land_details",
    Asset.CategoryChoices.HOUSE: "house_details",
    Asset.CategoryChoices.STOCK: "stock_details",
    Asset.CategoryChoices.BOND: "bond_details",
    Asset.CategoryChoices.OTHER: "other_details",
}

CATEGORY_LABELS = {
    Asset.CategoryChoices.VEHICLE: "Vehicles",
    Asset.CategoryChoices.LAND: "Land",
    Asset.CategoryChoices.HOUSE: "Houses",
    Asset.CategoryChoices.STOCK: "Stocks",
    Asset.CategoryChoices.BOND: "Government Bonds",
    Asset.CategoryChoices.OTHER: "Other Assets",
}

# Sidebar query parameter / alias routing -> actual Django category value.
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
    "other": Asset.CategoryChoices.OTHER,
    "others": Asset.CategoryChoices.OTHER,
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def _is_admin(user):
    """Check if user has admin privileges (superuser, staff, or ADMIN role)."""
    return user.is_authenticated and (
        user.is_superuser or user.is_staff or getattr(user, "role", "USER").upper() == "ADMIN"
    )


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
# DEDICATED CATEGORY LIST VIEWS
# ============================================================

@login_required
def vehicle_list(request):
    assets = Asset.objects.filter(owner=request.user, category=Asset.CategoryChoices.VEHICLE, status=Asset.StatusChoices.ACTIVE).order_by("-created_at")
    return render(request, "assets/vehicle_list.html", {"assets": assets, "asset_count": assets.count()})

@login_required
def land_list(request):
    assets = Asset.objects.filter(owner=request.user, category=Asset.CategoryChoices.LAND, status=Asset.StatusChoices.ACTIVE).order_by("-created_at")
    return render(request, "assets/land_list.html", {"assets": assets, "asset_count": assets.count()})

@login_required
def house_list(request):
    assets = Asset.objects.filter(owner=request.user, category=Asset.CategoryChoices.HOUSE, status=Asset.StatusChoices.ACTIVE).order_by("-created_at")
    return render(request, "assets/house_list.html", {"assets": assets, "asset_count": assets.count()})

@login_required
def stock_list(request):
    assets = Asset.objects.filter(owner=request.user, category=Asset.CategoryChoices.STOCK, status=Asset.StatusChoices.ACTIVE).order_by("-created_at")
    return render(request, "assets/stock_list.html", {"assets": assets, "asset_count": assets.count()})

@login_required
def bond_list(request):
    assets = Asset.objects.filter(owner=request.user, category=Asset.CategoryChoices.BOND, status=Asset.StatusChoices.ACTIVE).order_by("-created_at")
    return render(request, "assets/bond_list.html", {"assets": assets, "asset_count": assets.count()})

@login_required
def other_list(request):
    assets = Asset.objects.filter(owner=request.user, category=Asset.CategoryChoices.OTHER, status=Asset.StatusChoices.ACTIVE).order_by("-created_at")
    return render(request, "assets/other_list.html", {"assets": assets, "asset_count": assets.count()})


# ============================================================
# ASSET DETAIL VIEW
# ============================================================

@login_required
def asset_detail(request, asset_id):
    """Display comprehensive details, specifics, and linked documents for a single asset."""
    if _is_admin(request.user):
        asset = get_object_or_404(Asset, pk=asset_id)
    else:
        asset = get_object_or_404(Asset, pk=asset_id, owner=request.user)

    specific_detail = _get_asset_detail(asset)
    
    # Pre-process specific fields to avoid template underscore restrictions (_meta)
    specific_fields = []
    if specific_detail:
        for field in specific_detail._meta.fields:
            if field.name not in ['id', 'asset']:
                val = getattr(specific_detail, field.name, None)
                if val is not None and val != "":
                    specific_fields.append({
                        "label": field.verbose_name.title(),
                        "value": val
                    })

    documents = asset.documents.all() if hasattr(asset, 'documents') else AssetDocument.objects.filter(asset=asset)

    context = {
        "asset": asset,
        "specific_detail": specific_detail,
        "specific_fields": specific_fields,
        "documents": documents,
    }
    return render(request, "assets/asset_detail.html", context)


# ============================================================
# SUPPORTING DOCUMENTS & INTELLIGENCE VAULT
# ============================================================

@login_required
def asset_documents(request):
    """Display supporting documents belonging only to the logged-in user's assets."""
    documents = (
        AssetDocument.objects.filter(asset__owner=request.user)
        .select_related("asset", "uploaded_by")
        .order_by("-uploaded_at")
    )

    context = {
        "documents": documents,
        "document_count": documents.count(),
    }

    return render(request, "assets/asset_documents.html", context)


@login_required
def asset_map(request):
    """Renders the geographic map view for real estate and land parcels."""
    geo_assets = Asset.objects.filter(
        owner=request.user,
        status=Asset.StatusChoices.ACTIVE,
        category__in=[Asset.CategoryChoices.LAND, Asset.CategoryChoices.HOUSE]
    )
    
    context = {
        "geo_assets": geo_assets,
    }
    return render(request, "assets/asset_map.html", context)


@login_required
def asset_timeline(request):
    """Renders the chronological activity history and audit lifecycle of portfolio assets."""
    user_assets = Asset.objects.filter(owner=request.user).order_by("-created_at")
    
    context = {
        "user_assets": user_assets,
    }
    return render(request, "assets/asset_timeline.html", context)


# ============================================================
# GENERIC ASSET CREATION
# ============================================================

@login_required
def create_asset_generic(request, specific_form_class, category, title):
    """Create an asset, its category details, and an optional document."""

    if request.method == "POST":
        asset_form = AssetForm(request.POST)
        specific_form = specific_form_class(request.POST, request.FILES)
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
    return create_asset_generic(request, VehicleForm, Asset.CategoryChoices.VEHICLE, "Add New Vehicle")

@login_required
def create_land(request):
    return create_asset_generic(request, LandForm, Asset.CategoryChoices.LAND, "Add New Land")

@login_required
def create_house(request):
    return create_asset_generic(request, HouseForm, Asset.CategoryChoices.HOUSE, "Add New House")

@login_required
def create_stock(request):
    return create_asset_generic(request, StockForm, Asset.CategoryChoices.STOCK, "Add New Stock")

@login_required
def create_bond(request):
    return create_asset_generic(request, GovernmentBondForm, Asset.CategoryChoices.BOND, "Add Government Bond")

@login_required
def create_other(request):
    return create_asset_generic(request, OtherAssetForm, Asset.CategoryChoices.OTHER, "Add Other Asset")


# ============================================================
# ASSET UPDATE
# ============================================================

@login_required
def asset_update(request, asset_id):
    """Update an asset (any asset if admin, or user's own asset) and optionally add a document."""
    if _is_admin(request.user):
        asset = get_object_or_404(Asset, pk=asset_id)
    else:
        asset = get_object_or_404(Asset, pk=asset_id, owner=request.user)

    specific_form_class = CATEGORY_FORMS.get(asset.category)

    if specific_form_class is None:
        messages.error(request, "This asset category cannot be edited.")
        return redirect("assets:asset_list")

    specific_instance = _get_asset_detail(asset)

    if request.method == "POST":
        asset_form = AssetForm(request.POST, instance=asset)
        specific_form = specific_form_class(
            request.POST,
            request.FILES,
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
                    # Keep original owner if admin edits someone else's asset
                    if not updated_asset.owner_id:
                        updated_asset.owner = asset.owner
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
                if _is_admin(request.user):
                    return redirect("dashboards:admin_all_assets")
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


# ============================================================
# ASSET DELETE VIEW
# ============================================================

@login_required
def asset_delete(request, asset_id):
    """Delete an asset securely (any asset if admin, or user's own asset)."""
    if _is_admin(request.user):
        asset = get_object_or_404(Asset, pk=asset_id)
    else:
        asset = get_object_or_404(Asset, pk=asset_id, owner=request.user)

    if request.method == "POST":
        asset_name = asset.name
        asset.delete()
        messages.success(request, f"Asset '{asset_name}' was deleted successfully.")
        if _is_admin(request.user):
            return redirect("dashboards:admin_all_assets")
        return redirect("assets:asset_list")

    context = {
        "asset": asset,
    }
    return render(request, "assets/asset_confirm_delete.html", context)


# ============================================================
# INDIVIDUAL ASSET PDF REPORT GENERATOR
# ============================================================

@login_required
def asset_report_pdf(request, asset_id):
    """Generate and download a certified valuation report PDF for an individual asset."""
    if _is_admin(request.user):
        asset = get_object_or_404(Asset, pk=asset_id)
    else:
        asset = get_object_or_404(Asset, pk=asset_id, owner=request.user)

    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # Header Styling
        p.setFillColorRGB(0.03, 0.38, 0.44) # #086070
        p.rect(0, 735, 612, 60, fill=1, stroke=0)
        p.setFillColorRGB(1, 1, 1)
        p.setFont("Helvetica-Bold", 16)
        p.drawString(54, 755, "SECURED PRIVATE WEALTH PORTAL")
        p.setFont("Helvetica", 10)
        p.drawString(54, 740, "Official Certified Asset Valuation Report")

        # Asset Details Section
        p.setFillColorRGB(0.06, 0.09, 0.16)
        p.setFont("Helvetica-Bold", 14)
        p.drawString(54, 680, f"Asset: {asset.name}")
        
        p.setFont("Helvetica", 11)
        p.drawString(54, 650, f"Record ID: #{asset.id}")
        p.drawString(54, 630, f"Category: {asset.get_category_display()}")
        p.drawString(54, 610, f"Estimated Valuation: ${asset.current_estimated_value:,.2f}")
        owner_name = getattr(asset.owner, 'email', str(asset.owner))
        p.drawString(54, 590, f"Registered Owner: {owner_name}")
        p.drawString(54, 570, f"Verification Status: Certified Active")

        # Footer
        p.setFont("Helvetica-Oblique", 9)
        p.setFillColorRGB(0.4, 0.4, 0.4)
        p.drawString(54, 50, "This is an official computer-generated document from Assetra Private Wealth Portal.")

        p.showPage()
        p.save()

        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Asset_Report_{asset.id}.pdf"'
        return response

    except ImportError:
        # Fallback if ReportLab is not installed
        report_text = f"Asset Report #{asset.id}\n{asset.name}\nValuation: ${asset.current_estimated_value}"
        response = HttpResponse(report_text, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="Asset_Report_{asset.id}.txt"'
        return response