from var_dump import var_dump
import csv
import re
import os


class DataSet:
    def __init__(self, file_name, vacancies_objects):
        self.file_name = file_name
        self.vacancies_objects = vacancies_objects


class Vacancy:
    def __init__(self, name, description, key_skills, experience_id, premium,
                 employer_name, salary, area_name, published_at):
        self.name = name
        self.description = description
        self.key_skills = key_skills
        self.experience_id = experience_id
        self.premium = premium
        self.employer_name = employer_name
        self.salary = salary
        self.area_name = area_name
        self.published_at = published_at


class Salary:
    def __init__(self, salary_from, salary_to, salary_gross, salary_currency):
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_gross = salary_gross
        self.salary_currency = salary_currency


def fix_field(field):
    return ' '.join(re.sub(re.compile(r'<[^>]+>'), '', field).split())


def csv_reader(name):
    with open(name, encoding='utf-8-sig') as file:
        return [row for row in csv.DictReader(file)]


def csv_filer(rows):
    result = list()
    for row in rows:
        correct_row = True
        for field in row:
            if row[field] is None or len(row[field]) == 0:
                correct_row = False
                continue
        if correct_row:
            row['description'] = fix_field(row['description'])
            row['name'] = fix_field(row['name'])
            row['key_skills'] = row['key_skills'].split('\n')
            result.append(row)
    return result if len(result) != 0 else False


file_name = input("Введите название файла: ")
filter_string = input("Введите параметр фильтрации: ")
sort_string = input("Введите параметр сортировки: ")
reverse_sort = input("Обратный порядок сортировки (Да / Нет): ")
numbers = input("Введите диапазон вывода: ")
skills = input("Введите требуемые столбцы: ")

salary_keys = ['salary_from', 'salary_to', 'salary_gross', 'salary_currency']
vacancy_keys = ['name', 'description', 'key_skills', 'experience_id', 'premium', 'employer_name',
                object, 'area_name', 'published_at']

if os.stat(file_name).st_size == 0:
    print("Пустой файл")
else:
    answer = csv_reader(file_name)
    fix_data = csv_filer(answer)
    vacancies_objects = []
    if fix_data:
        for element in fix_data:
            salary = Salary(*[element[key] for key in salary_keys])
            vacancy = Vacancy(*[element[key] if key != object else salary for key in vacancy_keys])
            vacancies_objects.append(vacancy)
    data = DataSet(file_name, vacancies_objects)
    var_dump(data)
