import csv

answer = []
with open(input(), encoding='utf-8-sig') as file:
    reader = csv.reader(file)
    columns = next(reader)
    print(columns)
    for row in reader:
        if len(row) == len(columns) and not('' in row):
            answer.append(row)
print(answer)
