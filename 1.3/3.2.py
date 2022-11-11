import csv
import re

with open(input(), encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    for row in reader:
        correct_row = True
        for field in row:
            if row[field] is None or len(row[field]) == 0:
                correct_row = False
                continue
            row[field] = ' '.join(re.sub(re.compile(r'<[^>]+>'), '', row[field]).replace('\n', ', ').replace('\r\n', ', ').split())
        if correct_row:
            for field in row:
                print("{}: {}".format(field, row[field]))
            print()
