import os

def apply_fixes():
    # Ensure directories exist
    os.makedirs("dashboards", exist_ok=True)
    os.makedirs("templates/dashboards", exist_ok=True)

    # ---------------------------------------------------------
    # 1. REWRITE DASHBOARDS/VIEWS.PY TO FIX ROUTING
    # ---------------------------------------------------------
    views_content = """import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from portfolios.services import PortfolioEngine
from documents.models import Document
from assets.models import Asset
from support.models import Ticket
from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder

User = get_user_model()

@login_required
def role_router(request):
    if request.user.is_superuser or request.user.role == "ROLE_ADMIN": return redirect("admin_dashboard")
    elif request.user.role == "ROLE_MANAGER": return redirect("manager_dashboard")
    elif request.user.role == "ROLE_HELP_DESK": return redirect("helpdesk_dashboard")
    else: return redirect("user_dashboard")

@login_required
def user_dashboard(request):
    engine = PortfolioEngine(request.user)
    summary = engine.get_portfolio_summary()
    
    # Chart.js Data Prep
    dist_labels = [item['category'] for item in summary['distribution']] if summary['distribution'] else ['No Assets']
    dist_data = [float(item['total_value']) for item in summary['distribution']] if summary['distribution'] else [1]
    
    hist_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    hist_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, float(summary['total_current_value'])]

    context = {
        "summary": summary,
        "user": request.user,
        "assets": Asset.objects.filter(owner=request.user, status="ACTIVE"),
        "liquidity_ratio": engine.get_liquidity_profile(),
        "risk_exposure": engine.get_risk_exposure(),
        "chart_dist_labels": json.dumps(dist_labels, cls=DjangoJSONEncoder),
        "chart_dist_data": json.dumps(dist_data, cls=DjangoJSONEncoder),
        "chart_hist_labels": json.dumps(hist_labels, cls=DjangoJSONEncoder),
        "chart_hist_data": json.dumps(hist_data, cls=DjangoJSONEncoder),
    }
    # ROUTING FIX: Now pointing to the modern client dashboard
    return render(request, "dashboards/client_dashboard.html", context)

@login_required
def manager_dashboard(request):
    if not request.user.is_manager(): return redirect("role_router")
    pending = Document.objects.filter(status__in=["SUBMITTED", "UNDER_REVIEW"]).order_by("uploaded_at")
    
    # ROUTING FIX: Now pointing to the modern advisor dashboard
    return render(request, "dashboards/wealth_advisor_dashboard.html", {
        "documents": pending, 
        "compliance_score": "94.2%", 
        "avg_review_time": "1.4 Hours", 
        "flagged_accounts": 2
    })

@login_required
def admin_dashboard(request):
    if not request.user.is_admin(): return redirect("role_router")
    return render(request, "dashboards/admin_dashboard.html", {"total_system_assets": Asset.objects.count(), "active_users": User.objects.filter(is_active=True).count(), "system_health": "Optimal", "last_backup": "2 Hours Ago"})

@login_required
def helpdesk_dashboard(request):
    if not request.user.is_help_desk(): return redirect("role_router")
    open_tickets = Ticket.objects.filter(status__in=[Ticket.StatusChoices.OPEN, Ticket.StatusChoices.IN_PROGRESS]).order_by("-priority", "created_at")
    return render(request, "dashboards/helpdesk_dashboard.html", {"tickets": open_tickets, "open_ticket_count": open_tickets.count(), "locked_accounts": User.objects.filter(is_active=False).count(), "avg_response_time": "12 Mins"})
"""
    with open("dashboards/views.py", "w", encoding="utf-8") as f:
        f.write(views_content)
    print("[1/3] Successfully updated routing logic in dashboards/views.py")

    # ---------------------------------------------------------
    # 2. DYNAMIC CLIENT DASHBOARD TEMPLATE REPLACEMENT
    # ---------------------------------------------------------
    client_html = """{% extends 'base.html' %}
{% block content %}
<div class="min-h-screen bg-slate-950 text-slate-100 p-6 lg:p-10">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
        <div>
            <h1 class="text-3xl font-bold tracking-tight text-white">Private Wealth Portal: {{ request.user.get_full_name|default:request.user.username }}</h1>
            <p class="text-slate-400 text-sm">Traditional Asset Portfolio & Institutional Oversight</p>
        </div>
        <div class="flex items-center gap-4 bg-slate-900 border border-slate-800 p-2 rounded-xl">
            <span class="text-xs uppercase tracking-wider text-slate-400 font-semibold px-2">Valuation Mode:</span>
            <button id="toggleNetWorth" class="bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-medium px-4 py-2 rounded-lg transition shadow-md">
                Net Value (Post-Liabilities)
            </button>
        </div>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-6 shadow-xl backdrop-blur-md">
            <p class="text-xs font-medium text-slate-400 uppercase">Total Portfolio Valuation</p>
            <h3 class="text-2xl font-bold text-white mt-2">${{ summary.total_current_value|floatformat:2 }}</h3>
            <span class="text-emerald-400 text-xs font-semibold flex items-center mt-1">ROI: {{ summary.percentage_change|floatformat:2 }}%</span>
        </div>
        <div class="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-6 shadow-xl backdrop-blur-md">
            <p class="text-xs font-medium text-slate-400 uppercase">Invested Capital</p>
            <h3 class="text-2xl font-bold text-white mt-2">${{ summary.total_purchase_value|floatformat:2 }}</h3>
            <span class="text-slate-400 text-xs mt-1 block">Total Initial Acquisitions</span>
        </div>
        <div class="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-6 shadow-xl backdrop-blur-md">
            <p class="text-xs font-medium text-slate-400 uppercase">Liquidity Profile</p>
            <h3 class="text-2xl font-bold text-white mt-2">{{ liquidity_ratio }}</h3>
            <span class="text-emerald-400 text-xs font-semibold flex items-center mt-1">Liquid Assets / Total Value</span>
        </div>
        <div class="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-6 shadow-xl backdrop-blur-md">
            <p class="text-xs font-medium text-slate-400 uppercase">Risk Exposure</p>
            <h3 class="text-2xl font-bold text-amber-400 mt-2">{{ risk_exposure }}</h3>
            <span class="text-slate-400 text-xs mt-1 block">Based on Concentration limits</span>
        </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
        <div class="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-6 shadow-xl lg:col-span-1">
            <h2 class="text-lg font-semibold text-white mb-4">Asset Allocation</h2>
            <div class="relative h-64 flex items-center justify-center">
                <canvas id="assetDonutChart"></canvas>
            </div>
        </div>
        <div class="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-6 shadow-xl lg:col-span-2">
            <div class="flex justify-between items-center mb-4">
                <h2 class="text-lg font-semibold text-white">Historical Performance (12 Months)</h2>
                <a href="{% url 'portfolio_statement' %}" target="_blank" class="bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium px-3 py-1.5 rounded-lg border border-slate-700 transition">
                    Download Statement PDF
                </a>
            </div>
            <div class="relative h-64">
                <canvas id="performanceLineChart"></canvas>
            </div>
        </div>
    </div>

    <div class="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-6 shadow-xl mb-8">
        <h2 class="text-lg font-semibold text-white mb-4">Registered Holdings</h2>
        <div class="overflow-x-auto">
            <table class="w-full text-left text-sm text-slate-300">
                <thead class="bg-slate-800/50 text-xs uppercase text-slate-400">
                    <tr>
                        <th class="p-3">Asset / Property Name</th>
                        <th class="p-3">Category</th>
                        <th class="p-3">Portfolio Goal Tag</th>
                        <th class="p-3">Estimated Value</th>
                        <th class="p-3">Last Verified</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-slate-800">
                    {% for asset in assets %}
                    <tr>
                        <td class="p-3 font-medium text-white">{{ asset.name }}</td>
                        <td class="p-3">{{ asset.get_category_display }}</td>
                        <td class="p-3"><span class="bg-blue-950 text-blue-300 border border-blue-800 text-xs px-2.5 py-1 rounded-full">Active Hold</span></td>
                        <td class="p-3 cursor-pointer hover:text-emerald-400 transition">${{ asset.current_estimated_value|floatformat:2 }}</td>
                        <td class="p-3 text-slate-400">{{ asset.valuation_date|date:"Y-m-d" }}</td>
                    </tr>
                    {% empty %}
                    <tr><td colspan="5" class="p-3 text-center text-slate-500">No assets currently registered in portfolio.</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    const ctxDonut = document.getElementById('assetDonutChart').getContext('2d');
    new Chart(ctxDonut, {
        type: 'doughnut',
        data: {
            labels: JSON.parse('{{ chart_dist_labels|safe }}'),
            datasets: [{
                data: JSON.parse('{{ chart_dist_data|safe }}'),
                backgroundColor: ['#10b981', '#6366f1', '#f59e0b', '#3b82f6', '#ec4899'],
                borderWidth: 0
            }]
        },
        options: { responsive: true, maintainAspectRatio: false }
    });

    const ctxLine = document.getElementById('performanceLineChart').getContext('2d');
    new Chart(ctxLine, {
        type: 'line',
        data: {
            labels: JSON.parse('{{ chart_hist_labels|safe }}'),
            datasets: [{
                label: 'Portfolio Valuation ($)',
                data: JSON.parse('{{ chart_hist_data|safe }}'),
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                fill: true,
                tension: 0.3
            }]
        },
        options: { responsive: true, maintainAspectRatio: false }
    });
</script>
{% endblock %}"""
    with open("templates/dashboards/client_dashboard.html", "w", encoding="utf-8") as f:
        f.write(client_html)
    print("[2/3] Successfully integrated dynamic data into client_dashboard.html")

    # ---------------------------------------------------------
    # 3. DYNAMIC WEALTH ADVISOR TEMPLATE REPLACEMENT
    # ---------------------------------------------------------
    advisor_html = """{% extends 'base.html' %}
{% block content %}
<div class="min-h-screen bg-slate-950 text-slate-100 p-6 lg:p-10">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
        <div>
            <h1 class="text-3xl font-bold tracking-tight text-white">Wealth Advisor Console: {{ request.user.get_full_name|default:request.user.username }}</h1>
            <p class="text-slate-400 text-sm">Client Portfolio Oversight & Compliance Review Center</p>
        </div>
        <div class="flex items-center gap-3">
            <a href="{% url 'export_compliance_report' %}" class="bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-medium px-4 py-2.5 rounded-xl transition shadow-lg">
                Export Audit Report (PDF)
            </a>
        </div>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-6 shadow-xl backdrop-blur-md">
            <p class="text-xs font-medium text-slate-400 uppercase">Compliance Score</p>
            <h3 class="text-2xl font-bold text-white mt-2">{{ compliance_score }}</h3>
            <span class="text-emerald-400 text-xs font-semibold flex items-center mt-1">Platform Average</span>
        </div>
        <div class="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-6 shadow-xl backdrop-blur-md">
            <p class="text-xs font-medium text-slate-400 uppercase">Pending Document Reviews</p>
            <h3 class="text-2xl font-bold text-amber-400 mt-2">{{ documents.count }} Items</h3>
            <span class="text-slate-400 text-xs mt-1 block">Requires KYC Verification</span>
        </div>
        <div class="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-6 shadow-xl backdrop-blur-md">
            <p class="text-xs font-medium text-slate-400 uppercase">Flagged Accounts</p>
            <h3 class="text-2xl font-bold text-rose-400 mt-2">{{ flagged_accounts }} Accounts</h3>
            <span class="text-slate-400 text-xs mt-1 block">KYC Discrepancies</span>
        </div>
        <div class="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-6 shadow-xl backdrop-blur-md">
            <p class="text-xs font-medium text-slate-400 uppercase">SLA Compliance Rate</p>
            <h3 class="text-2xl font-bold text-emerald-400 mt-2">{{ avg_review_time }} Avg</h3>
            <span class="text-slate-400 text-xs mt-1 block">Time to Resolution</span>
        </div>
    </div>

    <div class="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-6 shadow-xl mb-8">
        <h2 class="text-lg font-semibold text-white mb-4">Document Verification Queue (SLA Monitoring)</h2>
        <div class="overflow-x-auto">
            <table class="w-full text-left text-sm text-slate-300">
                <thead class="bg-slate-800/50 text-xs uppercase text-slate-400">
                    <tr>
                        <th class="p-3">Document Title</th>
                        <th class="p-3">Client</th>
                        <th class="p-3">Uploaded Time</th>
                        <th class="p-3">Status</th>
                        <th class="p-3">Review Action</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-slate-800">
                    {% for doc in documents %}
                    <tr class="{% if doc.status == 'UNDER_REVIEW' %}bg-rose-950/20 border-l-4 border-rose-500{% else %}border-l-4 border-amber-500{% endif %}">
                        <td class="p-3 font-medium text-white">{{ doc.get_category_display }} - {{ doc.asset.name|default:"General" }}</td>
                        <td class="p-3">{{ doc.uploader.username }}</td>
                        <td class="p-3 text-slate-400">{{ doc.uploaded_at|timesince }} ago</td>
                        <td class="p-3"><span class="text-rose-400 font-semibold text-xs">{{ doc.get_status_display }}</span></td>
                        <td class="p-3 flex gap-2">
                            <form method="POST" action="{% url 'review_document' doc.id %}" style="display:inline;">
                                {% csrf_token %}
                                <button type="submit" name="action" value="approve" class="bg-emerald-600 hover:bg-emerald-500 text-white text-xs px-3 py-1 rounded-lg transition">Approve</button>
                                <button type="submit" name="action" value="reject" class="bg-rose-600 hover:bg-rose-500 text-white text-xs px-3 py-1 rounded-lg transition ml-2">Reject</button>
                            </form>
                        </td>
                    </tr>
                    {% empty %}
                    <tr><td colspan="5" class="p-3 text-center text-slate-500">No pending documents to review. Inbox zero achieved.</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}"""
    with open("templates/dashboards/wealth_advisor_dashboard.html", "w", encoding="utf-8") as f:
        f.write(advisor_html)
    print("[3/3] Successfully integrated dynamic data into wealth_advisor_dashboard.html")

if __name__ == "__main__":
    apply_fixes()