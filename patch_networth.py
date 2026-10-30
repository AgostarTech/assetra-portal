
import os

# Update models.py in assets to include liability amount if missing
asset_model = "assets/models.py"
with open(asset_model, "r", encoding="utf-8") as f:
    content = f.read()

if "liability_amount" not in content:
    # Insert liability_amount field into Asset model
    content = content.replace("current_estimated_value = ", "liability_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)\n    current_estimated_value = ")
    with open(asset_model, "w", encoding="utf-8") as f:
        f.write(content)
    print("Added liability_amount to Asset model.")

# Update portfolios/services.py
service_path = "portfolios/services.py"
with open(service_path, "r", encoding="utf-8") as f:
    svc_content = f.read()

if "total_liabilities" not in svc_content:
    old_summary = """    def get_portfolio_summary(self):
        assets = self.assets.all()
        total_purchase = sum(a.purchase_price for a in assets)
        total_current = sum(a.current_estimated_value for a in assets)"""
    
    new_summary = """    def get_portfolio_summary(self):
        assets = self.assets.all()
        total_purchase = sum(a.purchase_price for a in assets)
        total_current = sum(a.current_estimated_value for a in assets)
        total_liabilities = sum(a.liability_amount for a in assets)
        net_worth = total_current - total_liabilities"""
    
    svc_content = svc_content.replace(old_summary, new_summary)
    # Also inject into return dict
    svc_content = svc_content.replace("\"total_current_value\": total_current,", "\"total_current_value\": total_current,\n            \"total_liabilities\": total_liabilities,\n            \"net_worth_value\": net_worth,")
    
    with open(service_path, "w", encoding="utf-8") as f:
        f.write(svc_content)
    print("Updated PortfolioEngine with Net Worth and liabilities.")

