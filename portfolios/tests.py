from django.test import TestCase
from django.contrib.auth import get_user_model
from assets.models import Asset
from portfolios.services import PortfolioEngine
from decimal import Decimal

User = get_user_model()

class PortfolioEngineTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.asset1 = Asset.objects.create(
            owner=self.user,
            category=Asset.CategoryChoices.VEHICLE,
            name="Company Car",
            purchase_price=Decimal("20000.00"),
            purchase_date="2025-01-01",
            current_estimated_value=Decimal("15000.00"),
            valuation_date="2026-01-01"
        )
        self.asset2 = Asset.objects.create(
            owner=self.user,
            category=Asset.CategoryChoices.STOCK,
            name="Tech Stocks",
            purchase_price=Decimal("5000.00"),
            purchase_date="2025-06-01",
            current_estimated_value=Decimal("8000.00"),
            valuation_date="2026-01-01"
        )
        self.engine = PortfolioEngine(self.user)

    def test_total_purchase_value(self):
        self.assertEqual(self.engine.get_total_purchase_value(), Decimal("25000.00"))

    def test_total_current_value(self):
        self.assertEqual(self.engine.get_total_current_value(), Decimal("23000.00"))

    def test_absolute_value_change(self):
        self.assertEqual(self.engine.get_absolute_value_change(), Decimal("-2000.00"))
