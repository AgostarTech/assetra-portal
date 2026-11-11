import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


# ============================================================
# FILE VALIDATION
# ============================================================

def validate_asset_document_size(uploaded_file):
    """Limit each uploaded document to 10 MB."""
    max_size = 10 * 1024 * 1024  # 10 MB in bytes

    if uploaded_file.size > max_size:
        raise ValidationError(
            "Each supporting document must be 10 MB or smaller."
        )


def validate_asset_document_filename(uploaded_file):
    """Reject filenames containing path separators."""
    filename = os.path.basename(uploaded_file.name)

    if filename != uploaded_file.name or filename in ("", ".", ".."):
        raise ValidationError("Invalid document filename.")


# ============================================================
# CHOICES FOR OWNERSHIP & SHARES
# ============================================================

class AssetOwnership(models.TextChoices):
    INDIVIDUAL = "INDIVIDUAL", _("Individual (Personal)")
    COMPANY = "COMPANY", _("Company / Corporate")


class ShareType(models.TextChoices):
    PRIVATE = "PRIVATE", _("Privately Held Company")
    PUBLIC = "PUBLIC", _("Publicly Listed Company")
    DSE = "DSE", _("Dar es Salaam Stock Exchange (DSE)")


# ============================================================
# MAIN ASSET MODEL
# ============================================================

class Asset(models.Model):

    class CategoryChoices(models.TextChoices):
        VEHICLE = "VEHICLE", _("Vehicle")
        LAND = "LAND", _("Land")
        HOUSE = "HOUSE", _("House")
        STOCK = "STOCK", _("Stock (Company Shares)")
        BOND = "BOND", _("Government Bond")
        OTHER = "OTHER", _("Other Asset")

    class StatusChoices(models.TextChoices):
        ACTIVE = "ACTIVE", _("Active")
        ARCHIVED = "ARCHIVED", _("Archived")
        SOLD = "SOLD", _("Sold")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assets",
    )

    # Individual vs Company Asset Ownership Options
    ownership_type = models.CharField(
        max_length=20,
        choices=AssetOwnership.choices,
        default=AssetOwnership.INDIVIDUAL,
        help_text=_("Designates whether this asset is owned individually or under a corporate entity."),
    )

    company_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_("If owned by a company, specify the corporate entity name."),
    )

    category = models.CharField(
        max_length=20,
        choices=CategoryChoices.choices,
    )

    name = models.CharField(max_length=255)

    unique_reference = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=True,
    )

    # Financial details
    purchase_price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
    )

    purchase_date = models.DateField()

    liability_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
    )

    current_estimated_value = models.DecimalField(
        max_digits=15,
        decimal_places=2,
    )

    valuation_date = models.DateField()

    currency = models.CharField(
        max_length=3,
        default="USD",
        help_text="Three-letter currency code, e.g. USD or TZS.",
    )

    description = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
    )

    # Audit timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        ownership_label = "Company" if self.ownership_type == AssetOwnership.COMPANY else "Individual"
        return f"{self.name} ({self.get_category_display()}) - [{ownership_label}]"


# ============================================================
# VEHICLE DETAILS
# ============================================================

class Vehicle(models.Model):
    asset = models.OneToOneField(
        Asset,
        on_delete=models.CASCADE,
        related_name="vehicle_details",
    )

    registration_number = models.CharField(
        max_length=50,
        unique=True,
    )

    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()

    def __str__(self):
        return (
            f"{self.make} {self.model} "
            f"({self.registration_number})"
        )


# ============================================================
# LAND DETAILS
# ============================================================

class Land(models.Model):
    asset = models.OneToOneField(
        Asset,
        on_delete=models.CASCADE,
        related_name="land_details",
    )

    location = models.CharField(max_length=255)

    plot_reference = models.CharField(
        max_length=100,
        unique=True,
    )

    size = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    measurement_unit = models.CharField(
        max_length=50,
        default="Square Meters",
    )

    def __str__(self):
        return f"Plot {self.plot_reference} at {self.location}"


# ============================================================
# HOUSE DETAILS
# ============================================================

class House(models.Model):
    asset = models.OneToOneField(
        Asset,
        on_delete=models.CASCADE,
        related_name="house_details",
    )

    location = models.CharField(max_length=255)

    property_identification = models.CharField(
        max_length=100,
        unique=True,
    )

    building_information = models.TextField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return (
            f"House {self.property_identification} "
            f"at {self.location}"
        )


# ============================================================
# STOCK / COMPANY SHARES DETAILS
# ============================================================

class Stock(models.Model):
    asset = models.OneToOneField(
        Asset,
        on_delete=models.CASCADE,
        related_name="stock_details",
    )

    share_category = models.CharField(
        max_length=20,
        choices=ShareType.choices,
        default=ShareType.PRIVATE,
        help_text=_("Select whether shares are private, public global, or DSE listed."),
    )

    company = models.CharField(max_length=255)
    
    ticker = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text=_("Stock ticker symbol if listed (e.g., NMB, CRDB, VODA for DSE)."),
    )

    units = models.DecimalField(
        max_digits=15,
        decimal_places=4,
    )

    price_per_share = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
    )

    @property
    def total_shares_value(self):
        return self.units * self.price_per_share

    def __str__(self):
        return f"{self.units} shares of {self.company} ({self.ticker or 'Private'})"


# ============================================================
# GOVERNMENT BOND DETAILS
# ============================================================

class GovernmentBond(models.Model):
    asset = models.OneToOneField(
        Asset,
        on_delete=models.CASCADE,
        related_name="bond_details",
    )

    issuer = models.CharField(max_length=255)

    face_value = models.DecimalField(
        max_digits=15,
        decimal_places=2,
    )

    coupon_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Percentage, e.g. 5.50.",
    )

    maturity_date = models.DateField()

    def __str__(self):
        return f"{self.issuer} Bond maturing {self.maturity_date}"


# ============================================================
# OTHER ASSET DETAILS
# ============================================================

class OtherAsset(models.Model):
    asset = models.OneToOneField(
        Asset,
        on_delete=models.CASCADE,
        related_name="other_details",
    )

    asset_sub_type = models.CharField(
        max_length=150,
        help_text=_("Specify type of asset, e.g. Artwork, Machinery, Jewelry, etc."),
    )

    serial_number_or_identifier = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_("Any serial number or unique asset identifier."),
    )

    def __str__(self):
        return f"{self.asset_sub_type}: {self.asset.name}"


# ============================================================
# ASSET DOCUMENTS
# ============================================================

class AssetDocument(models.Model):

    class DocumentType(models.TextChoices):
        OWNERSHIP = "OWNERSHIP", _("Ownership Certificate")
        PURCHASE = "PURCHASE", _("Purchase Receipt or Agreement")
        VALUATION = "VALUATION", _("Valuation Report")
        REGISTRATION = "REGISTRATION", _("Registration Document")
        INSURANCE = "INSURANCE", _("Insurance Document")
        LEGAL = "LEGAL", _("Legal Document")
        FINANCIAL = "FINANCIAL", _("Financial Statement")
        TITLE_DEED = "TITLE_DEED", _("Title Deed")
        SHARE_CERTIFICATE = "SHARE_CERTIFICATE", _("Share Certificate")
        BOND_CERTIFICATE = "BOND_CERTIFICATE", _("Bond Certificate")
        OTHER = "OTHER", _("Other Supporting Document")

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="supporting_documents",
    )

    title = models.CharField(
        max_length=255,
        help_text="A descriptive name for the document.",
    )

    document_type = models.CharField(
        max_length=30,
        choices=DocumentType.choices,
        default=DocumentType.OTHER,
    )

    file = models.FileField(
        upload_to="asset_documents/%Y/%m/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["pdf", "jpg", "jpeg", "png"]
            ),
            validate_asset_document_size,
            validate_asset_document_filename,
        ],
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="uploaded_asset_documents",
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = "Asset Document"
        verbose_name_plural = "Asset Documents"

    def __str__(self):
        return f"{self.title} for {self.asset.name}"


# ============================================================
# ASSET VALUATION HISTORY
# ============================================================

class AssetValuationHistory(models.Model):
    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="valuation_history",
    )

    estimated_value = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )

    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-recorded_at"]
        verbose_name = "Asset Valuation History"
        verbose_name_plural = "Asset Valuation History"

    def __str__(self):
        return (
            f"{self.asset.name}: "
            f"{self.estimated_value} on "
            f"{self.recorded_at.strftime('%Y-%m-%d')}"
        )


# ============================================================
# ASSET TAGS
# ============================================================

class AssetTag(models.Model):
    name = models.CharField(max_length=50)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="asset_tags",
    )

    assets = models.ManyToManyField(
        Asset,
        related_name="custom_tags",
        blank=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "user"],
                name="unique_asset_tag_name_per_user",
            )
        ]
        ordering = ["name"]

    def __str__(self):
        return self.name


# ============================================================
# AUDIT LOG MODEL
# ============================================================

class AuditLog(models.Model):
    class ActionChoices(models.TextChoices):
        CREATE = "CREATE", _("Create")
        UPDATE = "UPDATE", _("Update")
        DELETE = "DELETE", _("Delete")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="asset_audit_logs",  # Fixed clash with audit app
    )
    action = models.CharField(max_length=20, choices=ActionChoices.choices)
    model_name = models.CharField(max_length=100)
    object_id = models.PositiveIntegerField()
    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"

    def __str__(self):
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M')}] {self.user} performed {self.action} on {self.model_name} (#{self.object_id})"