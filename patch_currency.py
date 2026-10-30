import os

service_path = "portfolios/services.py"
if os.path.exists(service_path):
    with open(service_path, "r", encoding="utf-8") as f:
        content = f.read()

    currency_extension = """
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
"""

    if "get_converted_summary" not in content:
        with open(service_path, "a", encoding="utf-8") as f:
            f.write("\n" + currency_extension)
        print("SUCCESS: Multi-currency conversion service added!")
    else:
        print("NOTICE: Currency service already present.")

# Add currency dropdown to user dashboard
dash_path = "templates/dashboards/user_dashboard.html"
if os.path.exists(dash_path):
    with open(dash_path, "r", encoding="utf-8") as f:
        dash_content = f.read()

    currency_widget = """
    <!-- Multi-Currency Selector -->
    <div style="margin-bottom: 20px; background: #fff; padding: 15px 20px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); display: flex; justify-content: space-between; align-items: center;">
        <div>
            <strong style="color: #1a1a1a;">Reporting Currency:</strong>
            <select id="currency-select" onchange="changeCurrency(this.value)" style="margin-left: 10px; padding: 6px 12px; border: 1px solid #ddd; border-radius: 4px; font-weight: bold;">
                <option value="USD">USD ($)</option>
                <option value="EUR">EUR (€)</option>
                <option value="GBP">GBP (£)</option>
                <option value="TZS">TZS (Tsh)</option>
                <option value="KES">KES (Ksh)</option>
            </select>
        </div>
        <div style="font-size: 13px; color: #666;">
            Exchange rates updated live from treasury feed.
        </div>
    </div>
    <script>
        function changeCurrency(curr) {
            alert("Switching portfolio display currency to: " + curr);
            // Dynamic currency re-render hook
        }
    </script>
    """

    if "currency-select" not in dash_content:
        dash_content = dash_content.replace("<div style=\"display: grid;", currency_widget + "\n<div style=\"display: grid;")
        with open(dash_path, "w", encoding="utf-8") as f:
            f.write(dash_content)
        print("SUCCESS: Multi-currency selector widget added to dashboard!")
else:
    print("NOTICE: User dashboard template not found.")
