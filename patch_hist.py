import os

hist_path = "assets/models.py"
if os.path.exists(hist_path):
    with open(hist_path, "r", encoding="utf-8") as f:
        content = f.read()

    valuation_model = """

class AssetValuationHistory(models.Model):
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE, related_name='valuation_history')
    estimated_value = models.DecimalField(max_digits=14, decimal_places=2)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.asset.name} - ${self.estimated_value} on {self.recorded_at.strftime('%Y-%m-%d')}"
"""

    if "AssetValuationHistory" not in content:
        with open(hist_path, "a", encoding="utf-8") as f:
            f.write("\n" + valuation_model)
        print("SUCCESS: AssetValuationHistory model added to assets/models.py!")
    else:
        print("NOTICE: AssetValuationHistory model already exists.")
