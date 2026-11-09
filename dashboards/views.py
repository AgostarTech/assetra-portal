import json
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, Permission
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.db.models import Count, ProtectedError, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from assets.models import Asset
from audit.models import AuditLog
from documents.models import Document
from portfolios.services import PortfolioEngine
from support.models import Ticket

User = get_user_model()

ADMIN_LOGIN_URL = "/accounts/login/"


def admin_check(user):
    """Allow only ADMIN role or superusers/staff."""
    if not user.is_authenticated:
        return False
    role = (getattr(user, "role", "USER") or "USER").upper()
    return user.is_superuser or user.is_staff or role == "ADMIN"


admin_required = user_passes_test(admin_check, login_url=ADMIN_LOGIN_URL)


@login_required
def role_router(request):
    """Route user to their specific dashboard based strictly on ADMIN vs USER."""
    if admin_check(request.user):
        return redirect("dashboards:admin_dashboard")
    return redirect("dashboards:user_dashboard")


@login_required
def user_dashboard(request):
    engine = PortfolioEngine(request.user)
    summary = engine.get_portfolio_summary()
    distribution = summary.get("distribution", [])

    dist_labels = [item["category"] for item in distribution] if distribution else ["No Assets"]
    dist_data = [float(item["total_value"]) for item in distribution] if distribution else [0]
    hist_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    hist_data = [0] * 12
    hist_data[timezone.localdate().month - 1] = float(summary.get("total_current_value") or 0)

    context = {
        "summary": summary,
        "user": request.user,
        "assets": Asset.objects.filter(owner=request.user, status=Asset.StatusChoices.ACTIVE),
        "liquidity_ratio": engine.get_liquidity_profile(),
        "risk_exposure": engine.get_risk_exposure(),
        "chart_dist_labels": json.dumps(dist_labels, cls=DjangoJSONEncoder),
        "chart_dist_data": json.dumps(dist_data, cls=DjangoJSONEncoder),
        "chart_hist_labels": json.dumps(hist_labels, cls=DjangoJSONEncoder),
        "chart_hist_data": json.dumps(hist_data, cls=DjangoJSONEncoder),
    }
    return render(request, "dashboards/client_dashboard.html", context)


@login_required
@admin_required
def admin_dashboard(request):
    active_assets = Asset.objects.filter(status=Asset.StatusChoices.ACTIVE)
    pending_documents = Document.objects.filter(
        status__in=[Document.StatusChoices.SUBMITTED, Document.StatusChoices.UNDER_REVIEW]
    ).select_related("uploader", "asset").order_by("uploaded_at")[:8]

    open_tickets = Ticket.objects.filter(
        status__in=[Ticket.StatusChoices.OPEN, Ticket.StatusChoices.IN_PROGRESS]
    ).select_related("user").order_by("-priority", "created_at")[:8]

    category_stats = list(
        active_assets.values("category")
        .annotate(asset_count=Count("id"), total_value=Sum("current_estimated_value"))
        .order_by("-total_value")
    )

    total_asset_value = active_assets.aggregate(total=Sum("current_estimated_value"))["total"] or Decimal("0.00")

    for item in category_stats:
        item["label"] = dict(Asset.CategoryChoices.choices).get(item["category"], item["category"])
        item["total_value"] = item["total_value"] or Decimal("0.00")
        item["percentage"] = round(float(item["total_value"] / total_asset_value * 100), 1) if total_asset_value > 0 else 0

    context = {
        "total_system_assets": Asset.objects.count(),
        "active_asset_count": active_assets.count(),
        "total_asset_value": total_asset_value,
        "active_users": User.objects.filter(is_active=True).count(),
        "total_users": User.objects.count(),
        "total_clients": User.objects.filter(role="USER").count(),
        "admin_users": User.objects.filter(role="ADMIN").count(),
        "documents": pending_documents,
        "tickets": open_tickets,
        "category_stats": category_stats,
        "recent_assets": Asset.objects.select_related("owner").order_by("-created_at")[:8],
        "recent_audit_logs": AuditLog.objects.select_related("user").order_by("-timestamp")[:10],
    }
    return render(request, "dashboards/admin_dashboard.html", context)


@login_required
@admin_required
@require_http_methods(["GET", "POST"])
def admin_manage_users(request):
    if request.method == "POST":
        # 1. Handle User Creation
        if request.POST.get("create_user") == "1":
            email = request.POST.get("email", "").strip()
            password = request.POST.get("password", "").strip()
            role = request.POST.get("role", "USER").strip().upper()

            if not email or not password:
                messages.error(request, "Email and password are required for new users.")
                return redirect("dashboards:admin_manage_users")

            if User.objects.filter(email=email).exists():
                messages.error(request, f"Email '{email}' already exists.")
                return redirect("dashboards:admin_manage_users")

            with transaction.atomic():
                is_admin = role == "ADMIN"
                User.objects.create_user(
                    email=email,
                    password=password,
                    role=role,
                    is_staff=is_admin,
                    is_superuser=is_admin,
                    is_active=True
                )
            messages.success(request, f"User account '{email}' created successfully.")
            return redirect("dashboards:admin_manage_users")

        # 2. Handle User Deletion
        delete_user_id = request.POST.get("delete_user_id", "").strip()
        if delete_user_id:
            target_user = User.objects.filter(pk=delete_user_id).first()
            if not target_user:
                messages.error(request, "The specified user account was not found.")
                return redirect("dashboards:admin_manage_users")

            if target_user.pk == request.user.pk:
                messages.error(request, "You cannot delete your own active account.")
            elif target_user.is_superuser:
                messages.error(request, "Cannot delete a superuser account.")
            else:
                uident = getattr(target_user, 'email', target_user.pk)
                try:
                    with transaction.atomic():
                        target_user.delete()
                    messages.success(request, f"User account '{uident}' has been deleted.")
                except ProtectedError:
                    messages.error(
                        request,
                        f"Cannot delete user '{uident}' because they have associated records (such as documents or assets). Please deactivate the user instead or remove dependent records first."
                    )
            return redirect("dashboards:admin_manage_users")

        # 3. Handle Role & Status Update
        user_id = request.POST.get("user_id", "").strip()
        new_role = request.POST.get("role", "").strip().upper()
        new_is_active = request.POST.get("is_active") == "on"

        valid_roles = {"USER", "ADMIN"}
        target_user = User.objects.filter(pk=user_id).first()

        if not target_user or new_role not in valid_roles:
            messages.error(request, "Invalid user or role selection.")
            return redirect("dashboards:admin_manage_users")

        if target_user.pk == request.user.pk:
            messages.error(request, "You cannot modify your own role here.")
            return redirect("dashboards:admin_manage_users")

        with transaction.atomic():
            target_user.role = new_role
            target_user.is_active = new_is_active
            is_admin = new_role == "ADMIN"
            target_user.is_staff = is_admin
            target_user.save(update_fields=["role", "is_active", "is_staff"])

        messages.success(request, f"Access settings updated for {getattr(target_user, 'email', target_user.pk)}.")
        return redirect("dashboards:admin_manage_users")

    search = request.GET.get("q", "").strip()
    users = User.objects.all().order_by("-date_joined")

    if search:
        users = users.filter(
            Q(email__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search)
        )

    context = {
        "users": users,
        "search": search,
        "total_users": User.objects.count(),
        "active_users_count": User.objects.filter(is_active=True).count(),
        "admin_users_count": User.objects.filter(Q(role="ADMIN") | Q(is_staff=True)).count(),
    }
    return render(request, "dashboards/admin_manage_users.html", context)


@login_required
@admin_required
def admin_groups_permissions(request):
    """View and manage user groups, roles, and system permissions."""
    groups = Group.objects.prefetch_related('permissions', 'user_set').all()
    permissions = Permission.objects.select_related('content_type').all()
    all_users = User.objects.filter(is_active=True).order_by("email")

    if request.method == "POST":
        action = request.POST.get("action")

        # 1. Create a new group
        if action == "create_group":
            group_name = request.POST.get("group_name", "").strip()
            if group_name:
                Group.objects.get_or_create(name=group_name)
                messages.success(request, f"Group '{group_name}' created successfully.")
            return redirect("dashboards:admin_groups_permissions")

        # 2. Delete an existing group
        elif action == "delete_group":
            group_id = request.POST.get("group_id")
            group = get_object_or_404(Group, pk=group_id)
            group_name = group.name
            group.delete()
            messages.success(request, f"Group '{group_name}' has been deleted.")
            return redirect("dashboards:admin_groups_permissions")

        # 3. Add a member to a group
        elif action == "add_member":
            group_id = request.POST.get("group_id")
            user_id = request.POST.get("user_id")
            group = get_object_or_404(Group, pk=group_id)
            target_user = get_object_or_404(User, pk=user_id)
            
            target_user.groups.add(group)
            uident = getattr(target_user, 'email', target_user.pk)
            messages.success(request, f"User '{uident}' added to group '{group.name}'.")
            return redirect("dashboards:admin_groups_permissions")

        # 4. Remove a member from a group
        elif action == "remove_member":
            group_id = request.POST.get("group_id")
            user_id = request.POST.get("user_id")
            group = get_object_or_404(Group, pk=group_id)
            target_user = get_object_or_404(User, pk=user_id)
            
            target_user.groups.remove(group)
            uident = getattr(target_user, 'email', target_user.pk)
            messages.success(request, f"User '{uident}' removed from group '{group.name}'.")
            return redirect("dashboards:admin_groups_permissions")

    context = {
        "groups": groups,
        "permissions": permissions,
        "all_users": all_users,
    }
    return render(request, "dashboards/admin_groups_permissions.html", context)


@login_required
@admin_required
def admin_all_assets(request):
    """View, search, and manage all assets registered across all system users."""
    asset_query = request.GET.get("q", "").strip()
    assets_list = Asset.objects.select_related("owner").all().order_by("-created_at")

    if asset_query:
        assets_list = assets_list.filter(
            Q(name__icontains=asset_query) | Q(category__icontains=asset_query) | Q(owner__email__icontains=asset_query)
        )

    paginator = Paginator(assets_list, 15)
    page_number = request.GET.get("page")
    assets = paginator.get_page(page_number)

    context = {
        "assets": assets,
        "search": asset_query,
        "total_assets": assets_list.count(),
    }
    return render(request, "dashboards/admin_all_assets.html", context)


@login_required
@admin_required
def admin_client_portfolios(request):
    """View aggregated portfolio distributions and valuations for all clients."""
    clients = User.objects.filter(role="USER")
    portfolio_data = []

    for client in clients:
        client_assets = Asset.objects.filter(owner=client)
        if hasattr(Asset, 'StatusChoices'):
            client_assets = client_assets.filter(status=Asset.StatusChoices.ACTIVE)
        
        client_total = client_assets.aggregate(total=Sum("current_estimated_value"))["total"] or Decimal("0.00")
        portfolio_data.append({
            "client": client,
            "asset_count": client_assets.count(),
            "total_value": client_total,
        })

    context = {
        "portfolio_data": portfolio_data,
    }
    return render(request, "dashboards/admin_client_portfolios.html", context)


@login_required
@admin_required
def admin_documents_kyc(request):
    """Manage and verify all uploaded KYC documents and files."""
    status_filter = request.GET.get("status", "").strip()
    documents = Document.objects.select_related("uploader", "asset").order_by("-uploaded_at")

    if status_filter:
        documents = documents.filter(status=status_filter)

    if request.method == "POST":
        doc_id = request.POST.get("doc_id")
        new_status = request.POST.get("status")
        doc = get_object_or_404(Document, pk=doc_id)
        doc.status = new_status
        doc.save(update_fields=["status"])
        messages.success(request, f"Document status updated to {new_status}.")
        return redirect("dashboards:admin_documents_kyc")

    context = {
        "documents": documents,
        "selected_status": status_filter,
    }
    return render(request, "dashboards/admin_documents_kyc.html", context)


@login_required
@admin_required
def admin_support_tickets(request):
    """View and resolve client support tickets and inquiries."""
    tickets = Ticket.objects.select_related("user").order_by("-created_at")

    if request.method == "POST":
        ticket_id = request.POST.get("ticket_id")
        new_status = request.POST.get("status")
        ticket = get_object_or_404(Ticket, pk=ticket_id)
        ticket.status = new_status
        ticket.save(update_fields=["status"])
        messages.success(request, f"Ticket #{ticket.pk} status updated.")
        return redirect("dashboards:admin_support_tickets")

    context = {
        "tickets": tickets,
    }
    return render(request, "dashboards/admin_support_tickets.html", context)


@login_required
@admin_required
def admin_audit_logs(request):
    """View comprehensive system audit logs and tracked activities."""
    logs_list = AuditLog.objects.select_related("user").order_by("-timestamp")
    
    paginator = Paginator(logs_list, 25)
    page_number = request.GET.get("page")
    audit_logs = paginator.get_page(page_number)

    context = {
        "audit_logs": audit_logs,
    }
    return render(request, "dashboards/admin_audit_logs.html", context)


@login_required
def client_statements(request):
    engine = PortfolioEngine(request.user)
    context = {
        "summary": engine.get_portfolio_summary(),
    }
    return render(request, "dashboards/statements.html", context)


@login_required
def client_documents(request):
    docs = Document.objects.filter(uploader=request.user).order_by("-uploaded_at")
    context = {"documents": docs}
    return render(request, "dashboards/documents.html", context)


@login_required
def client_support(request):
    user_tickets = Ticket.objects.filter(user=request.user).order_by("-created_at")
    context = {"tickets": user_tickets}
    return render(request, "dashboards/support.html", context)


@login_required
def client_profile(request):
    context = {"user": request.user}
    return render(request, "dashboards/profile.html", context)