
import json
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from assets.models import Asset
from audit.models import AuditLog
from documents.models import Document
from portfolios.services import PortfolioEngine
from support.models import Ticket

User = get_user_model()

ADMIN_LOGIN_URL = "/dashboard/"


# ============================================================
# ACCESS CONTROL
# ============================================================

def admin_check(user):
    """Allow only authenticated administrators and superusers."""
    return (
        user.is_authenticated
        and (
            user.is_superuser
            or getattr(user, "is_admin", False)
        )
    )


admin_required = user_passes_test(
    admin_check,
    login_url=ADMIN_LOGIN_URL,
)


def get_client_ip(request):
    """Return the direct client IP address when available."""
    return request.META.get("REMOTE_ADDR")


def record_admin_action(request, action, details=""):
    """Record administrative actions without modifying existing logs."""
    AuditLog.objects.create(
        user=request.user,
        action=action,
        path=request.path[:255],
        ip_address=get_client_ip(request),
        details=details,
    )


# ============================================================
# DASHBOARD ROUTING
# ============================================================

@login_required
def role_router(request):
    """Send authenticated users to the appropriate dashboard."""
    if admin_check(request.user):
        return redirect("dashboards:admin_dashboard")

    return redirect("dashboards:user_dashboard")


# ============================================================
# CLIENT DASHBOARD
# ============================================================

@login_required
def user_dashboard(request):
    """Client dashboard showing only the current user's portfolio."""
    engine = PortfolioEngine(request.user)
    summary = engine.get_portfolio_summary()

    distribution = summary.get("distribution", [])

    dist_labels = (
        [item["category"] for item in distribution]
        if distribution
        else ["No Assets"]
    )

    dist_data = (
        [float(item["total_value"]) for item in distribution]
        if distribution
        else [0]
    )

    hist_labels = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
    ]

    hist_data = [0] * 12
    hist_data[timezone.localdate().month - 1] = float(
        summary.get("total_current_value") or 0
    )

    context = {
        "summary": summary,
        "user": request.user,
        "assets": Asset.objects.filter(
            owner=request.user,
            status=Asset.StatusChoices.ACTIVE,
        ),
        "liquidity_ratio": engine.get_liquidity_profile(),
        "risk_exposure": engine.get_risk_exposure(),
        "chart_dist_labels": json.dumps(
            dist_labels, cls=DjangoJSONEncoder
        ),
        "chart_dist_data": json.dumps(
            dist_data, cls=DjangoJSONEncoder
        ),
        "chart_hist_labels": json.dumps(
            hist_labels, cls=DjangoJSONEncoder
        ),
        "chart_hist_data": json.dumps(
            hist_data, cls=DjangoJSONEncoder
        ),
    }

    return render(
        request,
        "dashboards/client_dashboard.html",
        context,
    )


# ============================================================
# ADMIN DASHBOARD
# ============================================================

@login_required
@admin_required
def admin_dashboard(request):
    """System-wide administrative overview."""

    active_assets = Asset.objects.filter(
        status=Asset.StatusChoices.ACTIVE
    )

    pending_documents = (
        Document.objects.filter(
            status__in=[
                Document.StatusChoices.SUBMITTED,
                Document.StatusChoices.UNDER_REVIEW,
            ]
        )
        .select_related("uploader", "asset")
        .order_by("uploaded_at")[:8]
    )

    open_tickets = (
        Ticket.objects.filter(
            status__in=[
                Ticket.StatusChoices.OPEN,
                Ticket.StatusChoices.IN_PROGRESS,
            ]
        )
        .select_related("user")
        .order_by("-priority", "created_at")[:8]
    )

    category_stats = list(
        active_assets.values("category")
        .annotate(
            asset_count=Count("id"),
            total_value=Sum("current_estimated_value"),
        )
        .order_by("-total_value")
    )

    total_asset_value = (
        active_assets.aggregate(
            total=Sum("current_estimated_value")
        )["total"]
        or Decimal("0.00")
    )

    recent_assets = (
        Asset.objects.select_related("owner")
        .order_by("-created_at")[:8]
    )

    recent_audit_logs = (
        AuditLog.objects.select_related("user")
        .order_by("-timestamp")[:10]
    )

    active_users = User.objects.filter(is_active=True).count()

    pending_count = Document.objects.filter(
        status__in=[
            Document.StatusChoices.SUBMITTED,
            Document.StatusChoices.UNDER_REVIEW,
        ]
    ).count()

    open_ticket_count = Ticket.objects.filter(
        status__in=[
            Ticket.StatusChoices.OPEN,
            Ticket.StatusChoices.IN_PROGRESS,
        ]
    ).count()

    for item in category_stats:
        item["label"] = dict(
            Asset.CategoryChoices.choices
        ).get(item["category"], item["category"])

        item["total_value"] = (
            item["total_value"] or Decimal("0.00")
        )

        if total_asset_value > 0:
            item["percentage"] = round(
                float(item["total_value"] / total_asset_value * 100),
                1,
            )
        else:
            item["percentage"] = 0

    context = {
        "total_system_assets": Asset.objects.count(),
        "active_asset_count": active_assets.count(),
        "total_asset_value": total_asset_value,
        "active_users": active_users,
        "inactive_users": User.objects.filter(
            is_active=False
        ).count(),
        "total_users": User.objects.count(),
        "total_clients": User.objects.filter(role="USER").count(),
        "admin_users": User.objects.filter(role="ADMIN").count(),
        "pending_count": pending_count,
        "open_ticket_count": open_ticket_count,
        "documents": pending_documents,
        "tickets": open_tickets,
        "category_stats": category_stats,
        "recent_assets": recent_assets,
        "recent_audit_logs": recent_audit_logs,
    }

    return render(
        request,
        "dashboards/admin_dashboard.html",
        context,
    )


# ============================================================
# ADMIN USER MANAGEMENT
# ============================================================

@login_required
@admin_required
@require_http_methods(["GET", "POST"])
def admin_manage_users(request):
    """Search and update user access using validated POST requests."""

    if request.method == "POST":
        user_id = request.POST.get("user_id", "").strip()
        new_role = request.POST.get("role", "").strip()
        new_is_active = request.POST.get("is_active") == "on"

        valid_roles = {
            User.RoleChoices.USER,
            User.RoleChoices.ADMIN,
        }

        if not user_id.isdigit():
            messages.error(request, "Invalid user account.")
            return redirect("dashboards:admin_manage_users")

        if new_role not in valid_roles:
            messages.error(request, "The selected role is invalid.")
            return redirect("dashboards:admin_manage_users")

        with transaction.atomic():
            target_user = get_object_or_404(
                User.objects.select_for_update(),
                pk=int(user_id),
            )

            if target_user.pk == request.user.pk:
                messages.error(
                    request,
                    "You cannot change your own role or account status here.",
                )
                return redirect("dashboards:admin_manage_users")

            if target_user.is_superuser:
                messages.error(
                    request,
                    "Superuser accounts cannot be modified through this page.",
                )
                return redirect("dashboards:admin_manage_users")

            currently_active_admin = (
                target_user.is_active
                and target_user.role == User.RoleChoices.ADMIN
            )

            will_remain_active_admin = (
                new_is_active
                and new_role == User.RoleChoices.ADMIN
            )

            if currently_active_admin and not will_remain_active_admin:
                other_active_admins = User.objects.filter(
                    is_active=True,
                    role=User.RoleChoices.ADMIN,
                ).exclude(pk=target_user.pk).count()

                active_superusers = User.objects.filter(
                    is_active=True,
                    is_superuser=True,
                ).count()

                if other_active_admins + active_superusers == 0:
                    messages.error(
                        request,
                        "You cannot deactivate or demote the last active administrator.",
                    )
                    return redirect("dashboards:admin_manage_users")

            old_role = target_user.role
            old_is_active = target_user.is_active

            target_user.role = new_role
            target_user.is_active = new_is_active
            target_user.save(
                update_fields=["role", "is_active"]
            )

            if (
                old_role != new_role
                or old_is_active != new_is_active
            ):
                record_admin_action(
                    request,
                    "USER_ACCESS_UPDATED",
                    (
                        f"Target user ID: {target_user.pk}; "
                        f"role: {old_role} -> {new_role}; "
                        f"active: {old_is_active} -> {new_is_active}"
                    ),
                )

        messages.success(
            request,
            f"Access settings updated for {target_user.username}.",
        )

        return redirect("dashboards:admin_manage_users")

    search = request.GET.get("q", "").strip()

    users = User.objects.all().order_by("-date_joined")

    if search:
        from django.db.models import Q

        users = users.filter(
            Q(username__icontains=search)
            | Q(email__icontains=search)
            | Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
        )
    context = {
        "users": users,
        "search": search,
        "total_users": users.count(),
        "active_users_count": User.objects.filter(
            is_active=True
        ).count(),
        "admin_users_count": User.objects.filter(
            role=User.RoleChoices.ADMIN
        ).count(),
    }

    return render(
        request,
        "dashboards/admin_manage_users.html",
        context,
    )
    
