CATEGORY_RULES = {
    "Payment": ["payment", "paid", "deducted", "refund", "charged", "transaction"],
    "Delivery": ["delivery", "delivered", "shipment", "shipping", "late", "parcel"],
    "Account": ["login", "password", "account", "otp", "sign in"],
    "Product": ["damaged", "broken", "wrong item", "defective", "product"],
}

HIGH_WORDS = ["blocked", "fraud", "deducted", "urgent", "charged twice", "not received"]
MEDIUM_WORDS = ["late", "pending", "damaged", "wrong", "failed", "refund"]


def analyze_ticket(text: str) -> dict:
    t = text.lower()
    scores = {
        category: sum(1 for keyword in keywords if keyword in t)
        for category, keywords in CATEGORY_RULES.items()
    }
    category = max(scores, key=scores.get)
    if scores[category] == 0:
        category = "General"

    if any(word in t for word in HIGH_WORDS):
        priority = "High"
    elif any(word in t for word in MEDIUM_WORDS):
        priority = "Medium"
    else:
        priority = "Low"

    matched = [w for w in HIGH_WORDS + MEDIUM_WORDS if w in t]
    confidence = min(0.95, 0.55 + 0.08 * max(scores.values()) + 0.04 * len(matched))

    signals = [
        f"Detected category: {category}",
        f"Priority estimated from ticket language: {priority}",
    ]
    if matched:
        signals.append("Signals found: " + ", ".join(sorted(set(matched))))

    return {
        "category": category,
        "priority": priority,
        "confidence": confidence,
        "signals": signals,
    }
