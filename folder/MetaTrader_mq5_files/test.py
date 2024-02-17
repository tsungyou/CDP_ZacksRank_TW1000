a = [1, 2, 3, 4, 5]
b = [a[i] > 1 for i in range(5)]
print(b.count(True))