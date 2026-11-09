# accounts/gateway.py
import random

class TanzanianPaymentGateway:
    @staticmethod
    def request_mno_checkout(phone_number, amount, reference_code, provider):
        """
        Simulates a free USSD push prompt for M-Pesa, Tigo Pesa, Airtel, or Halopesa in sandbox mode.
        """
        # In free sandbox mode, we simulate a successful USSD push dispatch
        return {
            "success": True, 
            "message": f"Simulated USSD push sent to {phone_number} via {provider} for {amount:,.2f} TZS. (Sandbox Mode - Free)",
            "transaction_id": f"SIM-TX-{random.randint(100000, 999999)}"
        }

    @staticmethod
    def request_bank_checkout(amount, reference_code, bank_name):
        """
        Simulates a free bank transfer checkout reference.
        """
        return {
            "success": True,
            "message": f"Simulated bank bill generated for {bank_name}. Use Ref: {reference_code}.",
            "transaction_id": f"SIM-BK-{random.randint(100000, 999999)}"
        }