
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

    context = {
        "summary": summary,
        "assets": assets,
        "user": request.user,
        "chart_dist_labels": json.dumps(list(allocation.keys())),
        "chart_dist_data": json.dumps(list(allocation.values())),
        "chart_hist_labels": json.dumps([]),
        "chart_hist_data": json.dumps([]),
        "liquidity_ratio": "Not available",
        "risk_exposure": "Not available",
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
