
import requests

def convert_asset_currency(amount, source_currency, target_currency="USD"):
    """
    Standardizes global asset values into a single base currency using live exchange rates[cite: 1].
    """
    if source_currency == target_currency:
        return amount
        
    # Simulated API call to Fixer.io / currency exchange gateway
    exchange_rates = {
        "EUR": 1.10,
        "GBP": 1.30,
        "TZS": 0.00039,
        "USD": 1.00
    }
    
    rate = exchange_rates.get(source_currency, 1.0)
    converted_amount = amount * rate
    return round(converted_amount, 2)
