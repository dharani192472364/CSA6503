import numpy as np

arr = np.array([10, 15, 20, 25, 30, 35])

even = arr[arr % 2 == 0]

print("Even Numbers:", even)
