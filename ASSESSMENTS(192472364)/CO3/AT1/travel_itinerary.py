import os
import json
from dotenv import load_dotenv
from google import genai

# ============================================================
# 1. LOAD API KEY SECURELY
# ============================================================

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY was not found in .env")
    exit()


# ============================================================
# 2. GET USER INPUT
# ============================================================

city = input("Enter city: ").strip()

budget_input = input("Enter budget in INR: ").strip()

interests_input = input(
    "Enter interests separated by commas (e.g., history, food, beach): "
).strip()


# ============================================================
# 3. VALIDATE INPUT
# ============================================================

if not city:
    print("ERROR: City cannot be empty.")
    exit()

try:
    budget = float(budget_input)

    if budget <= 0:
        print("ERROR: Budget must be greater than 0.")
        exit()

except ValueError:
    print("ERROR: Budget must be a valid number.")
    exit()

if not interests_input:
    print("ERROR: At least one interest must be provided.")
    exit()

interests = [
    item.strip()
    for item in interests_input.split(",")
    if item.strip()
]


# ============================================================
# 4. DETERMINE BUDGET TYPE
# ============================================================

low_budget = budget < 500

if low_budget:
    print("\nWARNING: Budget is low for a complete one-day itinerary.")
    print("Affordable individual food options will be suggested.")


# ============================================================
# 5. CREATE GEMINI PROMPT
# ============================================================

if low_budget:

    prompt = f"""
The user wants affordable food suggestions.

City: {city}
Available Budget: INR {budget}
Interests: {", ".join(interests)}

The budget is insufficient for a complete one-day itinerary.

Suggest individual affordable food options.

Rules:
- Use the exact city provided.
- Every option must cost less than or equal to the user's budget.
- Do NOT create a full-day itinerary.
- Do NOT calculate a total estimated cost.
- The user will choose only one option.
- Suggest several different affordable options.
- Suggest a realistic minimum budget for a complete one-day itinerary.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "city": "{city}",
    "budget": {budget},
    "interests": {json.dumps(interests)},
    "budget_status": "insufficient for full-day itinerary",
    "realistic_minimum_budget": 0,
    "affordable_options": [
        {{
            "option": "Food item",
            "description": "Short description",
            "estimated_cost": 0
        }}
    ]
}}
"""

else:

    prompt = f"""
Create a timed one-day travel itinerary.

City: {city}
Budget: INR {budget}
Interests: {", ".join(interests)}

Rules:
- Use the exact city provided.
- Create a realistic one-day itinerary.
- Include specific time slots.
- Activities must match the interests.
- Keep the total estimated cost within the budget.

Return ONLY valid JSON.
Do not include markdown or explanations.

Use exactly this structure:

{{
    "city": "{city}",
    "budget": {budget},
    "interests": {json.dumps(interests)},
    "budget_status": "sufficient",
    "realistic_minimum_budget": 0,
    "itinerary": [
        {{
            "time": "HH:MM AM - HH:MM AM",
            "activity": "Activity description",
            "estimated_cost": 0
        }}
    ],
    "total_estimated_cost": 0
}}
"""


# ============================================================
# 6. CALL GEMINI API
# ============================================================

try:

    # Create Gemini client
    client = genai.Client(api_key=api_key)

    # Send request to Gemini
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "temperature": 0.3,
            "response_mime_type": "application/json"
        }
    )

    # ========================================================
    # 7. PARSE JSON RESPONSE
    # ========================================================

    try:

        itinerary_data = json.loads(response.text)

    except json.JSONDecodeError:

        print("\nERROR: Gemini returned invalid JSON.")
        print("The response could not be parsed.")
        exit()


    # ========================================================
    # 8. DISPLAY COMMON INFORMATION
    # ========================================================

    print("\n")
    print("TRAVEL ITINERARY")
    print("=" * 60)

    print("City:", itinerary_data.get("city"))
    print("Budget: INR", itinerary_data.get("budget"))

    interests_data = itinerary_data.get("interests", [])

    if isinstance(interests_data, list):
        interests_display = ", ".join(
            str(item) for item in interests_data
        )
    else:
        interests_display = str(interests_data)

    print("Interests:", interests_display)

    print(
        "Budget Status:",
        itinerary_data.get(
            "budget_status",
            "Not specified"
        )
    )

    minimum_budget = itinerary_data.get(
        "realistic_minimum_budget"
    )

    if minimum_budget:
        print(
            "Realistic Minimum Budget: INR",
            minimum_budget
        )


    # ========================================================
    # 9. LOW-BUDGET OUTPUT
    # ========================================================

    if low_budget:

        print("\nAFFORDABLE FOOD OPTIONS")
        print("-" * 60)

        options = itinerary_data.get(
            "affordable_options",
            []
        )

        if not options:

            print("No affordable options were generated.")

        else:

            print(
                "Choose ANY ONE option that fits your budget:\n"
            )

            for index, option in enumerate(options, 1):

                print(
                    f"{index}. {option.get('option')}"
                )

                print(
                    "   Description:",
                    option.get("description")
                )

                print(
                    "   Estimated Cost: INR",
                    option.get("estimated_cost")
                )

                print()


    # ========================================================
    # 10. NORMAL ITINERARY OUTPUT
    # ========================================================

    else:

        print("\nITINERARY")
        print("-" * 60)

        itinerary = itinerary_data.get(
            "itinerary",
            []
        )

        if not itinerary:

            print(
                "No itinerary activities were generated."
            )

        else:

            for item in itinerary:

                print(
                    "\nTime:",
                    item.get("time")
                )

                print(
                    "Activity:",
                    item.get("activity")
                )

                print(
                    "Estimated Cost: INR",
                    item.get("estimated_cost")
                )

        print("\n" + "-" * 60)

        print(
            "Total Estimated Cost: INR",
            itinerary_data.get(
                "total_estimated_cost",
                0
            )
        )

    print("=" * 60)


# ============================================================
# 11. HANDLE API ERRORS
# ============================================================

except Exception as e:

    error_message = str(e).lower()

    # Rate limit / quota error
    if (
        "429" in error_message
        or "quota" in error_message
        or "rate limit" in error_message
    ):

        print(
            "\nERROR: Gemini API rate limit "
            "or quota exceeded."
        )

        print(
            "Please wait and try again later."
        )

    # Timeout error
    elif (
        "timeout" in error_message
        or "timed out" in error_message
    ):

        print(
            "\nERROR: Gemini API request timed out."
        )

        print(
            "Check your internet connection "
            "and try again."
        )

    # Other API errors
    else:

        print(
            "\nERROR: Gemini API request failed."
        )

        print("Details:", e)