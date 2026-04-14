# Read entire file
with open('data.txt') as f:
    text = f.read()

# Read line by line (best for large files)
with open('data.txt') as f:
    for line in f:
        print(line.strip())  # strip() removes \n

# Write to file ('w' = overwrite, 'a' = append)
with open('output.txt', 'w') as f:
    f.write('Hello, World!\n')

import csv

# Read CSV (each row becomes a dict)
with open('students.csv') as f:
    for row in csv.DictReader(f):
        print(f"{row['name']}: {row['grade']}")

# Write CSV
data = [{'name': 'Alice', 'grade': 95},
        {'name': 'Bob', 'grade': 87}]
with open('output.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'grade'])
    writer.writeheader()
    writer.writerows(data)
