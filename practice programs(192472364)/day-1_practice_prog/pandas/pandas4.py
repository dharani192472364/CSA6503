import pandas as pd

student = {
    "Name": ["Rahul", "Priya", "Kiran"],
    "Marks": [85, 90, 88]
}

df = pd.DataFrame(student)

average = df["Marks"].mean()

print("Average Marks:", average)