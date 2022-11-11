import csv
import re


def convert_bool(value):
    if value == "True":
        return "Да"
    return "Нет"


def fix_field(field):
    html_tags = re.compile(r'<[^>]+>')
    return ' '.join(re.sub(html_tags, '', field).replace('\n', ', ').split())


def csv_reader(file_name):
    with open(file_name, encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


def csv_filer(rows):
    rows_ans = list()
    for row in rows:
        correct_row = True
        for field in row:
            if row[field] is None or len(row[field]) == 0:
                correct_row = False
                continue
            row[field] = fix_field(row[field])
        if correct_row:
            row['premium'] = convert_bool(row['premium'])
            row['salary_gross'] = convert_bool(row['salary_gross'])
            rows_ans.append(row)
    return rows_ans if len(rows_ans) != 0 else False


def print_vacancies(data_vacancies, dic_naming):
    for row in data_vacancies:
        dict_translate = dict()
        for key, value in dic_naming.items():
            dict_translate[key] = row[value]
        for key, value in dict_translate.items():
            print(f'{key}: {value}')
        print()


keys = ["Название", "Описание", "Навыки", "Опыт работы", "Премиум-вакансия", "Компания", "Нижняя граница вилки оклада",
        "Верхняя граница вилки оклада", "Оклад указан до вычета налогов", "Идентификатор валюты оклада",
        "Название региона", "Дата и время публикации вакансии"]
data = csv_reader(input())
fix_data = csv_filer(data)
if fix_data:
    dic_translator = dict(zip(keys, fix_data[0].keys()))
    print_vacancies(fix_data, dic_translator)
