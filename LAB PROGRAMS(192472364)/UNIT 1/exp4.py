import pandas as pd

# Create a dictionary
data = {
    "Student Name": ["Alice", "Bob", "Charlie", "David", "Emma"],
    "Grade": ["A", "B+", "A+", "B", "A"]
}

# Create DataFrame
df = pd.DataFrame(data)

# Display DataFrame
print("Student DataFrame:")
print(df)