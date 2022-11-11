import csv
import re


def get_suffix_by_rubles(count):
    if count % 10 == 0 or 5 <= count % 10 <= 9 or 10 <= count % 100 <= 19:
        return 'рублей'
    elif 2 <= count % 10 <= 4:
        return 'рубля'
    else:
        return 'рубль'


def get_suffix_by_count(count):
    if count % 10 == 0 or 5 <= count % 10 <= 9 or 10 <= count % 100 <= 19:
        return 'раз'
    elif 2 <= count % 10 <= 4:
        return 'раза'
    else:
        return 'раз'


def get_suffix_by_vacancy(count):
    if count % 10 == 0 or 5 <= count % 10 <= 9 or 10 <= count % 100 <= 19:
        return 'вакансий'
    elif 2 <= count % 10 <= 4:
        return 'вакансии'
    else:
        return 'вакансия'


def print_salaries(elements: list, need_reverse: bool):
    elements.sort(key=lambda key: key['medium_salary'], reverse=need_reverse)
    index = 0
    for element in result:
        if index == 10:
            break
        else:
            index += 1
            print(
                f'    {index}) {element["name"]} в компании "{element["employer_name"]}" - {element["medium_salary"]} '
                f'{get_suffix_by_rubles(element["medium_salary"])} (г. {element["area_name"]})')


result = []
skills = dict()
html = re.compile(r'<[^>]+>')
with open(input(), encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        correct_row = True
        for field in row:
            if row[field] is None or len(row[field]) == 0:
                correct_row = False
                continue
            if field != "key_skills":
                row[field] = ' '.join(re.sub(html, '', row[field]).split())
        if correct_row:
            if row['salary_currency'] != "RUR":
                continue
            medium_salary = (int(row['salary_to'].replace('.0', '')) + int(row['salary_from'].replace('.0', ''))) // 2
            row['medium_salary'] = medium_salary
            for element in row['key_skills'].split("\n"):
                if element not in skills:
                    skills[element] = 0
                skills[element] += 1
            result.append(row)

print("Самые высокие зарплаты:")
print_salaries(result, True)

print("\nСамые низкие зарплаты:")
print_salaries(result, False)

skills = dict(sorted(skills.items(), key=lambda x: -x[1]))
print(f"\nИз {len(skills.keys())} скиллов, самыми популярными являются:")
index = 0
for k, v in skills.items():
    if index != 10:
        index += 1
        print(f'    {index}) {k} - упоминается {v} {get_suffix_by_count(v)}')
    else:
        break

cities = dict()
for element in result:
    if element["area_name"] not in cities:
        cities[element["area_name"]] = [0, 0]
    cities[element["area_name"]][1] += 1
    cities[element["area_name"]][0] += element["medium_salary"]
print(f"\nИз {len(cities.keys())} городов, самые высокие средние ЗП:")
cities = dict(sorted(cities.items(), key=lambda x: (-x[1][0] // x[1][1], x[0])))
index = 0
for key, value in cities.items():
    index += 1
    if index == 11:
        break
    else:
        print(f'    {index}) {key} - средняя зарплата {value[0]//value[1]} {get_suffix_by_rubles(value[0]//value[1])} '
              f'({value[1]} {get_suffix_by_vacancy(value[1])})')
