import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .services import PortfolioEngine


@login_required
def portfolio_dashboard(request):
    engine = PortfolioEngine(request.user)
    summary = engine.get_portfolio_summary()
    assets = engine.assets.all()

    # Build allocation data from the assets available to this user.
    allocation = {}
    for asset in assets:
        category = (
            asset.get_category_display()
            if hasattr(asset, "get_category_display")
            else getattr(asset, "category", "Other")
        ) or "Other"

        value = getattr(asset, "current_estimated_value", 0) or 0
        allocation[category] = allocation.get(category, 0) + float(value)

    # Fetch live liquidity and risk profiles from PortfolioEngine if available
    liquidity_ratio = getattr(engine, "get_liquidity_profile", lambda: "Active Portfolio")()
    risk_exposure = getattr(engine, "get_risk_exposure", lambda: "Balanced")()

    context = {
        "summary": summary,
        "assets": assets,
        "user": request.user,
        "chart_dist_labels": json.dumps(list(allocation.keys()) if allocation else ["No Assets"]),
        "chart_dist_data": json.dumps(list(allocation.values()) if allocation else [0]),
        "chart_hist_labels": json.dumps(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]),
        "chart_hist_data": json.dumps([float(summary.get("total_current_value", 0))] * 12),
        "liquidity_ratio": liquidity_ratio,
        "risk_exposure": risk_exposure,
    }

    return render(request, "portfolios/dashboard.html", context)


@login_required
def portfolio_statement(request):
    engine = PortfolioEngine(request.user)
    summary = engine.get_portfolio_summary()
    assets = engine.assets.all()

    context = {
        "summary": summary,
        "assets": assets,
        "user": request.user,
    }

    return render(request, "portfolios/statement.html", context)