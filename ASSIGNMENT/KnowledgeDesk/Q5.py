# KnowledgeDesk - Q5
# Context Window and Monthly Cost Calculation

CONTEXT_WINDOW = 8192
SYSTEM_PROMPT = 400
CONVERSATION_HISTORY = 600
CHUNK_SIZE = 512
ANSWER_BUDGET = 600

INPUT_COST_PER_1000 = 0.18
OUTPUT_COST_PER_1000 = 0.55
MONTHLY_QUERIES = 20000

# Calculate maximum k
fixed_tokens = SYSTEM_PROMPT + CONVERSATION_HISTORY + ANSWER_BUDGET
max_k = (CONTEXT_WINDOW - fixed_tokens) // CHUNK_SIZE

# Token usage
retrieved_tokens = max_k * CHUNK_SIZE
input_tokens = SYSTEM_PROMPT + CONVERSATION_HISTORY + retrieved_tokens
total_tokens = input_tokens + ANSWER_BUDGET

# Cost calculation
input_cost = (input_tokens / 1000) * INPUT_COST_PER_1000
output_cost = (ANSWER_BUDGET / 1000) * OUTPUT_COST_PER_1000
cost_per_query = input_cost + output_cost

monthly_cost = cost_per_query * MONTHLY_QUERIES
budget = 40000
remaining_budget = budget - monthly_cost

print("=" * 65)
print("KNOWLEDGEDESK - Q5 CONTEXT & COST CALCULATION")
print("=" * 65)

print("\n1. CONTEXT WINDOW CALCULATION")
print("-" * 65)

print(f"Context window              : {CONTEXT_WINDOW} tokens")
print(f"System prompt               : {SYSTEM_PROMPT} tokens")
print(f"Conversation history        : {CONVERSATION_HISTORY} tokens")
print(f"Chunk size                  : {CHUNK_SIZE} tokens")
print(f"Answer budget               : {ANSWER_BUDGET} tokens")

print("\nFormula:")
print("400 + 600 + (512 × k) + 600 <= 8192")

print(f"\nMaximum k                   : {max_k} chunks")
print(f"Retrieved tokens            : {retrieved_tokens}")
print(f"Total tokens used           : {total_tokens}")
print(f"Remaining context           : {CONTEXT_WINDOW - total_tokens} tokens")

print("\n2. COST CALCULATION")
print("-" * 65)

print(f"Input tokens per query      : {input_tokens}")
print(f"Output tokens per query     : {ANSWER_BUDGET}")

print(f"\nInput cost/query             : Rs. {input_cost:.5f}")
print(f"Output cost/query            : Rs. {output_cost:.2f}")
print(f"Total cost/query             : Rs. {cost_per_query:.5f}")

print(f"\nMonthly queries              : {MONTHLY_QUERIES}")
print(f"Monthly inference cost       : Rs. {monthly_cost:.2f}")
print(f"Monthly budget               : Rs. {budget:.2f}")
print(f"Remaining budget             : Rs. {remaining_budget:.2f}")

if monthly_cost <= budget:
    print("\nBudget Status                : WITHIN BUDGET")
else:
    print("\nBudget Status                : EXCEEDS BUDGET")

print("=" * 65)