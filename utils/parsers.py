import re
from typing import Dict, Any, Optional

def parse_bank_sms(text: str) -> Dict[str, Any]:
    """
    Parses common Indian bank SMS formats to extract transaction type, amount, and merchant/party.
    Returns a dictionary with 'amount', 'type', and 'merchant'.
    """
    result = {
        "amount": 0.0,
        "type": "unknown",
        "merchant": "unknown"
    }
    
    # 1. Extract Amount
    # Common patterns: Rs. 100, INR 1,500.00, Rs 50.0
    amount_match = re.search(r'(?:Rs\.?|INR)\s*([\d,]+\.?\d*)', text, re.IGNORECASE)
    if amount_match:
        try:
            amount_str = amount_match.group(1).replace(',', '')
            result["amount"] = float(amount_str)
        except ValueError:
            pass

    # 2. Extract Transaction Type
    text_lower = text.lower()
    if 'debited' in text_lower or 'sent' in text_lower or 'paid' in text_lower:
        result["type"] = "debit"
    elif 'credited' in text_lower or 'received' in text_lower:
        result["type"] = "credit"

    # 3. Extract Merchant/Party
    # Pattern: to VPA/party (e.g., 'to Swiggy', 'to merchant@upi', 'info: Zomato')
    # Or 'from' for credits
    if result["type"] == "debit":
        merchant_match = re.search(r'(?:to|towards|info:?)\s+([A-Za-z0-9@\.\s]+?)(?:\s+(?:on|ref|via|from)|\.|$)', text, re.IGNORECASE)
        if merchant_match:
            result["merchant"] = merchant_match.group(1).strip()
    elif result["type"] == "credit":
        merchant_match = re.search(r'(?:from|by)\s+([A-Za-z0-9@\.\s]+?)(?:\s+(?:on|ref|via|to)|\.|$)', text, re.IGNORECASE)
        if merchant_match:
            result["merchant"] = merchant_match.group(1).strip()

    return result

# Simple test cases for module validation
if __name__ == "__main__":
    test_sms_1 = "Your a/c no. XX1234 is debited for Rs. 450.00 on 12-OCT-23 to SWIGGY. UPI Ref no 123456789."
    test_sms_2 = "INR 1,200.50 credited to your A/c XX1234 from Ramesh@upi on 10/10/23."
    
    print(parse_bank_sms(test_sms_1))
    print(parse_bank_sms(test_sms_2))
