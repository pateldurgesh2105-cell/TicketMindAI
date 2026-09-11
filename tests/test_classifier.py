from src.classifier import analyze_ticket


def test_payment_ticket():
    result = analyze_ticket("Payment was deducted but order is still pending")
    assert result["category"] == "Payment"
    assert result["priority"] == "High"


def test_delivery_ticket():
    result = analyze_ticket("My delivery is late")
    assert result["category"] == "Delivery"
    assert result["priority"] == "Medium"
