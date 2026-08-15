import pandas as pd

student = {
    "Name": ["Rahul", "Priya", "Kiran"],
    "Age": [20, 21, 19],
    "Marks": [85, 90, 88]
}

df = pd.DataFrame(student)

print(df["Name"])
print(df["Marks"])