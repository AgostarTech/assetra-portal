from decimal import Decimal
from django.db.models import Sum, Count
from assets.models import Asset

class PortfolioEngine:
    def __init__(self, user):
        self.user = user
        self.assets = Asset.objects.filter(owner=user, status=Asset.StatusChoices.ACTIVE)

    def get_total_purchase_value(self):
        total = self.assets.aggregate(total=Sum('purchase_price'))['total']
        return total if total is not None else Decimal('0.00')

    def get_total_current_value(self):
        total = self.assets.aggregate(total=Sum('current_estimated_value'))['total']
        return total if total is not None else Decimal('0.00')

    def get_absolute_value_change(self):
        return self.get_total_current_value() - self.get_total_purchase_value()

    def get_percentage_value_change(self):
        purchase_total = self.get_total_purchase_value()
        if purchase_total == Decimal('0.00'): return Decimal('0.00')
        return (self.get_absolute_value_change() / purchase_total) * Decimal('100.00')

    def get_asset_distribution(self):
        return self.assets.values('category').annotate(
            count=Count('id'), total_value=Sum('current_estimated_value')
        ).order_by('-total_value')

    def get_liquidity_profile(self):
        """Maps structural liquidity: Stocks & Bonds are liquid; Land & Houses are illiquid."""
        liquid_assets = self.assets.filter(category__in=[Asset.CategoryChoices.STOCK, Asset.CategoryChoices.BOND])
        liquid_value = liquid_assets.aggregate(total=Sum('current_estimated_value'))['total'] or Decimal('0.00')
        total_value = self.get_total_current_value()
        
        if total_value == Decimal('0.00'): return "0.00%"
        ratio = (liquid_value / total_value) * Decimal('100.00')
        return f"{ratio:.2f}%"

    def get_risk_exposure(self):
        """Calculates risk based on structural concentration and historical volatility."""
        total = self.get_total_current_value()
        if total == Decimal('0.00'): return "Neutral"
        
        # Example logic: Over-concentration in a single asset class increases risk
        distribution = self.get_asset_distribution()
        if not distribution: return "Neutral"
        
        max_concentration = (distribution[0]['total_value'] / total) * Decimal('100.00')
        if max_concentration > 70: return "High (Over-Concentrated)"
        elif max_concentration > 40: return "Moderate"
        else: return "Low (Diversified)"

    def get_portfolio_summary(self):
        return {
            'total_purchase_value': self.get_total_purchase_value(),
            'total_current_value': self.get_total_current_value(),
            'absolute_change': self.get_absolute_value_change(),
            'percentage_change': self.get_percentage_value_change(),
            'distribution': self.get_asset_distribution(),
            'asset_count': self.assets.count(),
        }


    def get_converted_summary(self, target_currency="USD"):
        summary = self.get_portfolio_summary()
        rates = {
            "USD": 1.0,
            "EUR": 0.92,
            "GBP": 0.79,
            "TZS": 2600.0,
            "KES": 130.0
        }
        rate = rates.get(target_currency, 1.0)
        
        return {
            "currency": target_currency,
            "total_current_value": round(summary["total_current_value"] * rate, 2),
            "total_liabilities": round(summary["total_liabilities"] * rate, 2),
            "net_worth_value": round(summary["net_worth_value"] * rate, 2),
        }


    def check_pending_valuations(self):
        from django.utils import timezone
        from datetime import timedelta
        from assets.models import Asset
        
        one_year_ago = timezone.now() - timedelta(days=365)
        stale_assets = Asset.objects.filter(updated_at__lt=one_year_ago)
        return stale_assets
