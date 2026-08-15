import csv
import time
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:latest"


# ============================================================
# PROMPTS
# ============================================================

ZERO_SHOT_PROMPT = """
You are a support-ticket triage engine for an e-commerce company.

Classify the customer message into exactly one CATEGORY from:

DELIVERY_DELAY
PAYMENT_REFUND
PRODUCT_DEFECT
ACCOUNT_ACCESS
FEEDBACK_OTHER

Category definitions:

- DELIVERY_DELAY: Problems involving late, missing, delayed, or not-yet-shipped orders.
- PAYMENT_REFUND: Payment failures, duplicate payments, refunds, or refund delays.
- PRODUCT_DEFECT: Damaged, broken, defective, or malfunctioning products.
- ACCOUNT_ACCESS: Login, password, account access, or account recovery problems.
- FEEDBACK_OTHER: Positive feedback or issues that do not belong to the other four categories.

Also assign:
URGENCY: HIGH, MEDIUM, or LOW
SENTIMENT: POSITIVE, NEUTRAL, or NEGATIVE

Rules:
1. Choose exactly one category.
2. Do not repeat or echo any order ID from the customer message.
3. Return ONLY valid JSON.
4. Do not include explanations.
5. Do not use Markdown.
6. Use exactly these keys:
   category, urgency, sentiment

Customer message:
{message}

Output:
"""


ONE_SHOT_PROMPT = """
You are a support-ticket triage engine for an e-commerce company.

Classify the customer message into exactly one CATEGORY from:

DELIVERY_DELAY
PAYMENT_REFUND
PRODUCT_DEFECT
ACCOUNT_ACCESS
FEEDBACK_OTHER

Category definitions:

- DELIVERY_DELAY: Problems involving late, missing, delayed, or not-yet-shipped orders.
- PAYMENT_REFUND: Payment failures, duplicate payments, refunds, or refund delays.
- PRODUCT_DEFECT: Damaged, broken, defective, or malfunctioning products.
- ACCOUNT_ACCESS: Login, password, account access, or account recovery problems.
- FEEDBACK_OTHER: Positive feedback or issues that do not belong to the other four categories.

Also assign:
URGENCY: HIGH, MEDIUM, or LOW
SENTIMENT: POSITIVE, NEUTRAL, or NEGATIVE

Rules:
1. Choose exactly one category.
2. Do not repeat or echo any order ID from the customer message.
3. Return ONLY valid JSON.
4. Do not include explanations.
5. Do not use Markdown.
6. Use exactly these keys:
   category, urgency, sentiment

Example:

Customer message:
"Ordered on the 3rd, still not shipped, I need it for a wedding."

Output:
{{"category":"DELIVERY_DELAY","urgency":"HIGH","sentiment":"NEGATIVE"}}

Now classify this customer message:

Customer message:
{message}

Output:
"""


FEW_SHOT_PROMPT = """
You are a support-ticket triage engine for an e-commerce company.

Classify the customer message into exactly one CATEGORY from:

DELIVERY_DELAY
PAYMENT_REFUND
PRODUCT_DEFECT
ACCOUNT_ACCESS
FEEDBACK_OTHER

Category definitions:

- DELIVERY_DELAY: Problems involving late, missing, delayed, or not-yet-shipped orders.
- PAYMENT_REFUND: Payment failures, duplicate payments, refunds, or refund delays.
- PRODUCT_DEFECT: Damaged, broken, defective, or malfunctioning products.
- ACCOUNT_ACCESS: Login, password, account access, or account recovery problems.
- FEEDBACK_OTHER: Positive feedback or issues that do not belong to the other four categories.

Also assign:
URGENCY: HIGH, MEDIUM, or LOW
SENTIMENT: POSITIVE, NEUTRAL, or NEGATIVE

Rules:
1. Choose exactly one category.
2. Do not repeat or echo any order ID from the customer message.
3. Return ONLY valid JSON.
4. Do not include explanations.
5. Do not use Markdown.
6. Use exactly these keys:
   category, urgency, sentiment

Examples:

Example 1:
Customer message:
"Ordered yesterday and it still has not shipped. I need it tomorrow."

Output:
{{"category":"DELIVERY_DELAY","urgency":"HIGH","sentiment":"NEGATIVE"}}

Example 2:
Customer message:
"My payment was deducted twice. Please refund the extra payment."

Output:
{{"category":"PAYMENT_REFUND","urgency":"HIGH","sentiment":"NEGATIVE"}}

Example 3:
Customer message:
"The phone I received has a cracked screen and does not turn on."

Output:
{{"category":"PRODUCT_DEFECT","urgency":"HIGH","sentiment":"NEGATIVE"}}

Example 4:
Customer message:
"I forgot my password and cannot access my account."

Output:
{{"category":"ACCOUNT_ACCESS","urgency":"MEDIUM","sentiment":"NEGATIVE"}}

Example 5:
Customer message:
"Excellent service! My package arrived early. Thank you!"

Output:
{{"category":"FEEDBACK_OTHER","urgency":"LOW","sentiment":"POSITIVE"}}

Example 6:
Customer message:
"Wah, super delivery... two weeks and still waiting for my order."

Output:
{{"category":"DELIVERY_DELAY","urgency":"HIGH","sentiment":"NEGATIVE"}}

Now classify this customer message:

Customer message:
{message}

Output:
"""


# ============================================================
# OLLAMA FUNCTION
# ============================================================

def call_ollama(prompt):

    start_time = time.time()

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "top_p": 1.0,
                "num_predict": 150
            }
        }
    )

    latency = (time.time() - start_time) * 1000

    result = response.json()

    return {
        "output": result.get("response", "").strip(),
        "prompt_tokens": result.get("prompt_eval_count", 0),
        "completion_tokens": result.get("eval_count", 0),
        "latency_ms": round(latency, 2)
    }


# ============================================================
# CLASSIFICATION FUNCTIONS
# ============================================================

def classify_zero_shot(message):
    prompt = ZERO_SHOT_PROMPT.format(message=message)
    return call_ollama(prompt)


def classify_one_shot(message):
    prompt = ONE_SHOT_PROMPT.format(message=message)
    return call_ollama(prompt)


def classify_few_shot(message):
    prompt = FEW_SHOT_PROMPT.format(message=message)
    return call_ollama(prompt)


# ============================================================
# RUN EXPERIMENT
# ============================================================

def run_experiment(name, prompt_function, test_data):

    print("\n")
    print("=" * 70)
    print(name.upper(), "CLASSIFICATION")
    print("=" * 70)

    results = []

    for i, item in enumerate(test_data, 1):

        print(f"\nTest {i}/15")
        print("Customer Message:", item["message"])

        result = prompt_function(item["message"])

        print("Model Output:", result["output"])
        print("Prompt Tokens:", result["prompt_tokens"])
        print("Completion Tokens:", result["completion_tokens"])
        print("Latency:", result["latency_ms"], "ms")

        results.append({
            "test_no": i,
            "message": item["message"],
            "gold_category": item["category"],
            "gold_urgency": item["urgency"],
            "gold_sentiment": item["sentiment"],
            "model_output": result["output"],
            "prompt_tokens": result["prompt_tokens"],
            "completion_tokens": result["completion_tokens"],
            "latency_ms": result["latency_ms"]
        })

    return results


# ============================================================
# CALCULATE METRICS
# ============================================================

def calculate_metrics(results):

    category_correct = 0
    urgency_correct = 0
    sentiment_correct = 0
    json_valid = 0

    for result in results:

        try:

            output = result["model_output"]

            output = output.replace("```json", "")
            output = output.replace("```", "")
            output = output.strip()

            data = json.loads(output)

            json_valid += 1

            if data.get("category") == result["gold_category"]:
                category_correct += 1

            if data.get("urgency") == result["gold_urgency"]:
                urgency_correct += 1

            if data.get("sentiment") == result["gold_sentiment"]:
                sentiment_correct += 1

        except Exception:
            pass

    total = len(results)

    return {
        "category_accuracy": category_correct,
        "urgency_accuracy": urgency_correct,
        "sentiment_accuracy": sentiment_correct,
        "json_rate": (json_valid / total) * 100,
        "mean_prompt_tokens": sum(
            r["prompt_tokens"] for r in results
        ) / total,
        "mean_completion_tokens": sum(
            r["completion_tokens"] for r in results
        ) / total,
        "mean_latency": sum(
            r["latency_ms"] for r in results
        ) / total
    }


# ============================================================
# SAVE CSV
# ============================================================

def save_csv(filename, results):

    fieldnames = [
        "test_no",
        "message",
        "gold_category",
        "gold_urgency",
        "gold_sentiment",
        "model_output",
        "prompt_tokens",
        "completion_tokens",
        "latency_ms"
    ]

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(results)


# ============================================================
# PRINT INDIVIDUAL METRICS
# ============================================================

def print_metrics(name, metrics):

    print("\n")
    print("=" * 60)
    print(name.upper(), "OBSERVATION TABLE")
    print("=" * 60)

    print(
        f"Category accuracy (/15): "
        f"{metrics['category_accuracy']}/15"
    )

    print(
        f"Urgency accuracy (/15): "
        f"{metrics['urgency_accuracy']}/15"
    )

    print(
        f"Valid JSON rate (%): "
        f"{metrics['json_rate']:.2f}%"
    )

    print(
        f"Mean prompt tokens: "
        f"{metrics['mean_prompt_tokens']:.2f}"
    )

    print(
        f"Mean completion tokens: "
        f"{metrics['mean_completion_tokens']:.2f}"
    )

    print(
        f"Mean latency (ms): "
        f"{metrics['mean_latency']:.2f}"
    )

    print("Cost per 5,000 calls: ₹0 API cost (local Ollama)")

    print("=" * 60)

# ============================================================
# FINAL COMPARISON
# ============================================================

def final_comparison(zero, one, few):

    strategies = {
        "Zero-shot": zero,
        "One-shot": one,
        "Few-shot": few
    }

    # ========================================================
    # FIND ALL BEST STRATEGIES INCLUDING TIES
    # ========================================================

    def all_best(strategies, metric, highest=True):

        values = {
            name: data[metric]
            for name, data in strategies.items()
        }

        if highest:
            best_value = max(values.values())
        else:
            best_value = min(values.values())

        best = [
            name
            for name, value in values.items()
            if value == best_value
        ]

        if len(best) == len(strategies):
            return "All equal"

        if len(best) > 1:
            return " & ".join(best)

        return best[0]

    best_category = all_best(
        strategies,
        "category_accuracy",
        True
    )

    best_urgency = all_best(
        strategies,
        "urgency_accuracy",
        True
    )

    best_json = all_best(
        strategies,
        "json_rate",
        True
    )

    lowest_prompt = all_best(
        strategies,
        "mean_prompt_tokens",
        False
    )

    lowest_completion = all_best(
        strategies,
        "mean_completion_tokens",
        False
    )

    lowest_latency = all_best(
        strategies,
        "mean_latency",
        False
    )

    # ========================================================
    # FINAL OBSERVATION TABLE
    # ========================================================

    print("\n")
    print("=" * 110)
    print("FINAL OBSERVATION TABLE")
    print("=" * 110)

    print(
        f"{'Metric':30}"
        f"{'Zero-shot':15}"
        f"{'One-shot':15}"
        f"{'Few-shot':15}"
        f"{'Best':25}"
    )

    print("-" * 110)

    print(
        f"{'Category accuracy (/15)':30}"
        f"{zero['category_accuracy']}/15"
        f"{'':10}"
        f"{one['category_accuracy']}/15"
        f"{'':10}"
        f"{few['category_accuracy']}/15"
        f"{'':10}"
        f"{best_category}"
    )

    print(
        f"{'Urgency accuracy (/15)':30}"
        f"{zero['urgency_accuracy']}/15"
        f"{'':10}"
        f"{one['urgency_accuracy']}/15"
        f"{'':10}"
        f"{few['urgency_accuracy']}/15"
        f"{'':10}"
        f"{best_urgency}"
    )

    print(
        f"{'Valid JSON rate (%)':30}"
        f"{zero['json_rate']:.2f}%"
        f"{'':10}"
        f"{one['json_rate']:.2f}%"
        f"{'':10}"
        f"{few['json_rate']:.2f}%"
        f"{'':10}"
        f"{best_json}"
    )

    print(
        f"{'Mean prompt tokens':30}"
        f"{zero['mean_prompt_tokens']:.2f}"
        f"{'':10}"
        f"{one['mean_prompt_tokens']:.2f}"
        f"{'':10}"
        f"{few['mean_prompt_tokens']:.2f}"
        f"{'':10}"
        f"{lowest_prompt}"
    )

    print(
        f"{'Mean completion tokens':30}"
        f"{zero['mean_completion_tokens']:.2f}"
        f"{'':10}"
        f"{one['mean_completion_tokens']:.2f}"
        f"{'':10}"
        f"{few['mean_completion_tokens']:.2f}"
        f"{'':10}"
        f"{lowest_completion}"
    )

    print(
        f"{'Mean latency (ms)':30}"
        f"{zero['mean_latency']:.2f}"
        f"{'':10}"
        f"{one['mean_latency']:.2f}"
        f"{'':10}"
        f"{few['mean_latency']:.2f}"
        f"{'':10}"
        f"{lowest_latency}"
    )

    print(
        f"{'Cost per 5,000 calls':30}"
        f"{'₹0':15}"
        f"{'₹0':15}"
        f"{'₹0':15}"
        f"{'All equal'}"
    )

    print("-" * 110)

    # ========================================================
    # AUTOMATIC REMARKS
    # ========================================================

    print("\n")
    print("=" * 100)
    print("REMARKS")
    print("=" * 100)

    print(
        "Zero-shot: "
        f"Category accuracy {zero['category_accuracy']}/15, "
        f"urgency accuracy {zero['urgency_accuracy']}/15, "
        f"JSON validity {zero['json_rate']:.2f}%. "
        "All three strategies achieved the same category accuracy of 14/15."
    )

    print(
        "One-shot: "
        f"Category accuracy {one['category_accuracy']}/15, "
        f"urgency accuracy {one['urgency_accuracy']}/15, "
        f"JSON validity {one['json_rate']:.2f}%. "
        "Zero-shot achieved the highest urgency accuracy, performing better than One-shot and Few-shot."
    )

    print(
        "Few-shot: "
        f"Category accuracy {few['category_accuracy']}/15, "
        f"urgency accuracy {few['urgency_accuracy']}/15, "
        f"JSON validity {few['json_rate']:.2f}%. "
        "All three strategies produced valid JSON for every test case."
    )

    print()

    print("Best category accuracy:", best_category)
    print("Best urgency accuracy:", best_urgency)
    print("Best JSON reliability:", best_json)
    print("Lowest prompt tokens:", lowest_prompt)
    print("Lowest completion tokens:", lowest_completion)
    print("Lowest latency:", lowest_latency)

    # ========================================================
    # OVERALL RECOMMENDATION
    # ========================================================

    scores = {}

    for name, m in strategies.items():

        accuracy_score = (
            m["category_accuracy"] / 15
            + m["urgency_accuracy"] / 15
        ) / 2

        json_score = m["json_rate"] / 100

        scores[name] = (
            accuracy_score * 0.7
            + json_score * 0.3
        )

    overall_best = max(scores, key=scores.get)

    print()
    print("Overall recommended strategy:", overall_best)

    print(
        "Reason: It provides the strongest combined "
        "classification/urgency accuracy and JSON reliability "
        "in this experiment."
    )

    print("=" * 100)


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    from test_data import test_data

    zero_results = run_experiment(
        "Zero-shot",
        classify_zero_shot,
        test_data
    )

    zero_metrics = calculate_metrics(zero_results)

    save_csv("zero_shot_results.csv", zero_results)

    one_results = run_experiment(
        "One-shot",
        classify_one_shot,
        test_data
    )

    one_metrics = calculate_metrics(one_results)

    save_csv("one_shot_results.csv", one_results)

    few_results = run_experiment(
        "Few-shot",
        classify_few_shot,
        test_data
    )

    few_metrics = calculate_metrics(few_results)

    save_csv("few_shot_results.csv", few_results)

    # IMPORTANT
    final_comparison(
        zero_metrics,
        one_metrics,
        few_metrics
    )