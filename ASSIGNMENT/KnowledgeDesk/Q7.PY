import math

# KnowledgeDesk - Q7
# Corpus, Chunk and Vector Index Size Calculation

DOCUMENTS = 12000
PAGES_PER_DOCUMENT = 8
TOKENS_PER_PAGE = 500

CHUNK_SIZE = 512
OVERLAP = 50

EMBEDDING_DIMENSIONS = 768
BYTES_PER_FLOAT32 = 4

# Corpus calculation
total_pages = DOCUMENTS * PAGES_PER_DOCUMENT
total_tokens = total_pages * TOKENS_PER_PAGE

# Chunk calculation
effective_tokens = CHUNK_SIZE - OVERLAP
number_of_chunks = math.ceil(
    (total_tokens - OVERLAP) / effective_tokens
)

# Vector index calculation
bytes_per_vector = EMBEDDING_DIMENSIONS * BYTES_PER_FLOAT32
total_vector_bytes = number_of_chunks * bytes_per_vector

# Convert to GB
vector_size_gb = total_vector_bytes / (1024 ** 3)

print("=" * 65)
print("KNOWLEDGEDESK - Q7 CORPUS & VECTOR INDEX CALCULATION")
print("=" * 65)

print("\n1. CORPUS SIZE")
print("-" * 65)

print(f"Number of documents       : {DOCUMENTS}")
print(f"Average pages/document    : {PAGES_PER_DOCUMENT}")
print(f"Tokens/page               : {TOKENS_PER_PAGE}")
print(f"Total pages               : {total_pages:,}")
print(f"Total corpus tokens       : {total_tokens:,}")

print("\n2. CHUNK CALCULATION")
print("-" * 65)

print(f"Chunk size                : {CHUNK_SIZE} tokens")
print(f"Overlap                   : {OVERLAP} tokens")
print(f"Effective new tokens      : {effective_tokens}")

print("\nFormula:")
print("ceil((48,000,000 - 50) / (512 - 50))")

print(f"\nNumber of chunks          : {number_of_chunks:,}")

print("\n3. VECTOR INDEX SIZE")
print("-" * 65)

print(f"Embedding dimensions      : {EMBEDDING_DIMENSIONS}")
print(f"Data type                 : float32")
print(f"Bytes per value           : {BYTES_PER_FLOAT32}")
print(f"Bytes per vector          : {bytes_per_vector:,}")
print(f"Total vector bytes        : {total_vector_bytes:,}")
print(f"Vector index size         : {vector_size_gb:.2f} GB")

print("\n4. STORAGE LIMIT CHECK")
print("-" * 65)

print("Storage limit             : 100 GB")

if vector_size_gb <= 100:
    print("Storage Status            : WITHIN LIMIT")
else:
    print("Storage Status            : EXCEEDS LIMIT")

print("=" * 65)