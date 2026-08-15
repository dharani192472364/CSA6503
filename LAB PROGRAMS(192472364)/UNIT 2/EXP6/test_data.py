
test_data = [
    {
        "message": "Ordered on the 3rd, still not shipped, I need it for a wedding.",
        "category": "DELIVERY_DELAY",
        "urgency": "HIGH",
        "sentiment": "NEGATIVE"
    },
    {
        "message": "Refund shows credited but nothing in my bank account since 9 days.",
        "category": "PAYMENT_REFUND",
        "urgency": "HIGH",
        "sentiment": "NEGATIVE"
    },
    {
        "message": "The headphones I received are broken. Left side has no sound.",
        "category": "PRODUCT_DEFECT",
        "urgency": "MEDIUM",
        "sentiment": "NEGATIVE"
    },
    {
        "message": "I forgot my password and cannot login to my account.",
        "category": "ACCOUNT_ACCESS",
        "urgency": "MEDIUM",
        "sentiment": "NEGATIVE"
    },
    {
        "message": "Great service! My order arrived earlier than expected.",
        "category": "FEEDBACK_OTHER",
        "urgency": "LOW",
        "sentiment": "POSITIVE"
    },
    {
        "message": "Where???",
        "category": "DELIVERY_DELAY",
        "urgency": "MEDIUM",
        "sentiment": "NEGATIVE"
    },
    {
        "message": "Wah, amazing delivery... ordered two weeks ago and still waiting.",
        "category": "DELIVERY_DELAY",
        "urgency": "HIGH",
        "sentiment": "NEGATIVE"
    },
    {
        "message": "Payment deducted twice for the same order. Please refund one payment.",
        "category": "PAYMENT_REFUND",
        "urgency": "HIGH",
        "sentiment": "NEGATIVE"
    },
    {
        "message": "Product looks nice but the screen is cracked. Need replacement.",
        "category": "PRODUCT_DEFECT",
        "urgency": "HIGH",
        "sentiment": "NEGATIVE"
    },
    {
        "message": "Login avvatledu, password correct ga enter chesina kuda.",
        "category": "ACCOUNT_ACCESS",
        "urgency": "MEDIUM",
        "sentiment": "NEGATIVE"
    },
    {
        "message": "Order 78451239 is late. Please don't repeat the order number in your response.",
        "category": "DELIVERY_DELAY",
        "urgency": "MEDIUM",
        "sentiment": "NEGATIVE"
    },
    {
        "message": "The app is easy to use and the shopping experience was excellent.",
        "category": "FEEDBACK_OTHER",
        "urgency": "LOW",
        "sentiment": "POSITIVE"
    },
    {
        "message": "I cannot access my account and I also need a refund for the cancelled order.",
        "category": "ACCOUNT_ACCESS",
        "urgency": "HIGH",
        "sentiment": "NEGATIVE"
    },
    {
        "message": "Yaar, payment ho gaya but refund abhi tak nahi aaya.",
        "category": "PAYMENT_REFUND",
        "urgency": "HIGH",
        "sentiment": "NEGATIVE"
    },
    {
        "message": "The delivery was late, but customer support was helpful and solved my issue quickly.",
        "category": "DELIVERY_DELAY",
        "urgency": "MEDIUM",
        "sentiment": "POSITIVE"
    }
]
test_data = [
    {
        "message": "Ordered on the 3rd, still not shipped, I need it for a wedding.",
        "category": "DELIVERY_DELAY",
        "urgency": "HIGH",
        "sentiment": "NEGATIVE"
    },
    {
        "message": "Refund shows credited but nothing in my bank account since 9 days.",
        "category": "PAYMENT_REFUND",
        "urgency": "HIGH",
        "sentiment": "NEGATIVE"
    },
    {
        "message": "The headphones I received are broken. Left side has no sound.",
        "category": "PRODUCT_DEFECT",
        "urgency": "MEDIUM",
        "sentiment": "NEGATIVE"
    },
    {
        "message": "I forgot my password and cannot login to my account.",
        "category": "ACCOUNT_ACCESS",
        "urgency": "MEDIUM",
        "sentiment": "NEGATIVE"
    },
    {
        "message": "Great service! My order arrived earlier than expected.",
        "category": "FEEDBACK_OTHER",
        "urgency": "LOW",
        "sentiment": "POSITIVE"
    },
    {
        "message": "Where???",
        "category": "DELIVERY_DELAY",
        "urgency": "MEDIUM",
        "sentiment": "NEGATIVE"
    },
    {
        "message": "Wah, amazing delivery... ordered two weeks ago and still waiting.",
        "category": "DELIVERY_DELAY",
        "urgency": "HIGH",
        "sentiment": "NEGATIVE"
    },
    {
        "message": "Payment deducted twice for the same order. Please refund one payment.",
        "category": "PAYMENT_REFUND",
        "urgency": "HIGH",
        "sentiment": "NEGATIVE"
    },
    {
        "message": "Product looks nice but the screen is cracked. Need replacement.",
        "category": "PRODUCT_DEFECT",
        "urgency": "HIGH",
        "sentiment": "NEGATIVE"
    },
    {
        "message": "Login avvatledu, password correct ga enter chesina kuda.",
        "category": "ACCOUNT_ACCESS",
        "urgency": "MEDIUM",
        "sentiment": "NEGATIVE"
    },
    {
        "message": "Order 78451239 is late. Please don't repeat the order number in your response.",
        "category": "DELIVERY_DELAY",
        "urgency": "MEDIUM",
        "sentiment": "NEGATIVE"
    },
    {
        "message": "The app is easy to use and the shopping experience was excellent.",
        "category": "FEEDBACK_OTHER",
        "urgency": "LOW",
        "sentiment": "POSITIVE"
    },
    {
        "message": "I cannot access my account and I also need a refund for the cancelled order.",
        "category": "ACCOUNT_ACCESS",
        "urgency": "HIGH",
        "sentiment": "NEGATIVE"
    },
    {
        "message": "Yaar, payment ho gaya but refund abhi tak nahi aaya.",
        "category": "PAYMENT_REFUND",
        "urgency": "HIGH",
        "sentiment": "NEGATIVE"
    },
    {
        "message": "The delivery was late, but customer support was helpful and solved my issue quickly.",
        "category": "DELIVERY_DELAY",
        "urgency": "MEDIUM",
        "sentiment": "POSITIVE"
    }
]

print("Total test messages:", len(test_data))

for i, item in enumerate(test_data, 1):
    print(i, item)