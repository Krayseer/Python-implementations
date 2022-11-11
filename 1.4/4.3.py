from prettytable import PrettyTable
import csv
import re
import os


def convert_bool(value):
    if value == "True":
        return "Да"
    return "Нет"


def convert_tax(bool_value):
    if bool_value.lower() != "да":
        return "С вычетом налогов"
    return "Без вычета налогов"


def fix_salary_value(salary):
    return (salary.replace('.0', '')[:-3] + ' ' + salary.replace('.0', '')[-3:]).lstrip()


def fix_field(field):
    html_tags = re.compile(r'<[^>]+>')
    return ' '.join(re.sub(html_tags, '', field).replace('\n', ', ').split())


def get_date(datetime):
    return ".".join(reversed(datetime[:datetime.index("T")].split('-')))


def line_trim(dictionary, tag_value):
    if len(dictionary[tag_value]) > 100:
        dictionary[tag_value] = dictionary[tag_value][:100] + "..."
    return dictionary[tag_value]


def csv_reader(name):
    with open(name, encoding='utf-8-sig') as file:
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


def formatter(row):
    keys = ["Название", "Описание", "Навыки", "Опыт работы", "Премиум-вакансия", "Компания",
            "Нижняя граница вилки оклада",
            "Верхняя граница вилки оклада", "Оклад указан до вычета налогов", "Идентификатор валюты оклада",
            "Название региона", "Дата публикации вакансии"]

    currency_key_eng = ['AZN', 'BYR', 'EUR', 'GEL', 'KGS', 'KZT', 'RUR', 'UAH', 'USD', 'UZS']
    currency_key_rus = ["Манаты", "Белорусские рубли", "Евро", "Грузинский лари", "Киргизский сом", "Тенге", "Рубли",
                        "Гривны", "Доллары", "Узбекский сум"]

    experience_key_eng = ["noExperience", "between1And3", "between3And6", "moreThan6"]
    experience_key_rus = ["Нет опыта", "От 1 года до 3 лет", "От 3 до 6 лет", "Более 6 лет"]

    translate_tags = ['Верхняя граница вилки оклада', "Нижняя граница вилки оклада",
                      "Оклад указан до вычета налогов", "Идентификатор валюты оклада"]

    currency_dict = dict(zip(currency_key_eng, currency_key_rus))
    experience_dict = dict(zip(experience_key_eng, experience_key_rus))

    row['salary_currency'] = currency_dict[row['salary_currency']]
    row['experience_id'] = experience_dict[row['experience_id']]
    row['key_skills'] = row['key_skills'].replace(', ', '\n')

    translate_dict = dict()
    for key, value in dict(zip(keys, row.keys())).items():
        translate_dict[key] = row[value]

    result_dict = dict()
    counter = 0
    for key, value in translate_dict.items():
        if key not in translate_tags:
            result_dict[key] = value
        else:
            counter += 1
            if counter == 3:
                salary_from = translate_dict['Нижняя граница вилки оклада']
                salary_to = translate_dict['Верхняя граница вилки оклада']
                result_dict['Оклад'] = f"{fix_salary_value(salary_from)} - {fix_salary_value(salary_to)} " \
                                       f"({translate_dict['Идентификатор валюты оклада']}) " \
                                       f"({convert_tax(translate_dict['Оклад указан до вычета налогов'])})"
    result_dict['Дата публикации вакансии'] = get_date(result_dict['Дата публикации вакансии'])
    result_dict['Навыки'] = line_trim(result_dict, 'Навыки')
    result_dict['Описание'] = line_trim(result_dict, 'Описание')

    return result_dict


def print_vacancies(data_vacancies):
    count = 1
    vacancy_table = PrettyTable()
    vacancy_table.hrules = 1
    vacancy_table.align = "l"

    if not data_vacancies:
        print("Нет данных")
    else:
        for row in data_vacancies:
            row = {"№": count, **formatter(row)}
            vacancy_table.field_names = row.keys()
            vacancy_table.add_row(list(row.values()))
            count += 1
        vacancy_table._max_width = {field: 20 for field in vacancy_table.field_names}
        print(vacancy_table)


file_name = input()
data = csv_reader(file_name)
fix_data = csv_filer(data)
if os.stat(file_name).st_size == 0:
    print("Пустой файл")
else:
    print_vacancies(fix_data)