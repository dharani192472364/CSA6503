import matplotlib.pyplot as plt

subjects = ["Math", "Science", "English", "Computer"]
marks = [80, 90, 75, 95]

plt.bar(subjects, marks)
plt.title("Student Marks")
plt.xlabel("Subjects")
plt.ylabel("Marks")

plt.show()