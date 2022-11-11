from prettytable import PrettyTable
import csv
import re
import os


def convert_bool(value):
    return "Да" if value == "True" else "Нет"


def convert_bool_reverse(value):
    return True if value == "Да" else False


def convert_tax(bool_value):
    return "С вычетом налогов" if bool_value.lower() != "да" else "Без вычета налогов"


def fix_salary_value(salary):
    return (salary.replace('.0', '')[:-3] + ' ' + salary.replace('.0', '')[-3:]).lstrip()


def fix_field(field):
    return ' '.join(re.sub(re.compile(r'<[^>]+>'), '', field).split())


def get_date(datetime):
    return ".".join(reversed(datetime[:datetime.index('T')].split('-')))


def line_trim(dictionary, tag_value):
    return dictionary[tag_value][:100] + '...' if len(dictionary[tag_value]) > 100 else dictionary[tag_value]


def row_trim(row):
    for key in list(row.keys())[1:]:
        row[key] = line_trim(row, key)
    return row


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
            row['premium'] = convert_bool(row['premium'])
            row['salary_gross'] = convert_bool(row['salary_gross'])
            result.append(row)
    return result if len(result) != 0 else False


def formatter(row):
    keys = ["Название", "Описание", "Навыки", "Опыт работы", "Премиум-вакансия", "Компания",
            "Нижняя граница вилки оклада", "Верхняя граница вилки оклада", "Оклад указан до вычета налогов",
            "Идентификатор валюты оклада", "Название региона", "Дата публикации вакансии"]

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

    translate_dict = dict()
    for key, value in dict(zip(keys, row.keys())).items():
        translate_dict[key] = row[value]

    result = dict()
    counter = 0
    for key, value in translate_dict.items():
        if key not in translate_tags:
            result[key] = value
        else:
            counter += 1
            if counter == 3:
                salary_from = translate_dict['Нижняя граница вилки оклада']
                salary_to = translate_dict['Верхняя граница вилки оклада']
                result['Оклад'] = f"{fix_salary_value(salary_from)} - {fix_salary_value(salary_to)} " \
                                  f"({translate_dict['Идентификатор валюты оклада']}) " \
                                  f"({convert_tax(translate_dict['Оклад указан до вычета налогов'])})"
    return result


def print_vacancies(data_vacancies, filter_string, sort_string, reverse_sort, numbers, skills):
    count = 1
    vacancy_table = PrettyTable()
    vacancy_table.hrules = 1
    vacancy_table.align = "l"

    filter_string = filter_string.split(": ")
    numbers_none = len(numbers) == 0
    skills_none = len(skills) == 0

    usual_tags = ["Дата публикации вакансии", "Опыт работы", "Премиум-вакансия", "Название региона",
                  "Компания", "Название", "Описание"]

    currency_key = ["Манаты", "Белорусские рубли", "Евро", "Грузинский лари", "Киргизский сом", "Тенге", "Рубли",
                    "Гривны", "Доллары", "Узбекский сум"]
    currency_value = [35.68, 23.91, 59.00, 21.74, 0.76, 0.13, 1, 1.64, 60.66, 0.0055]
    currency_dict = dict(zip(currency_key, currency_value))

    if not data_vacancies:
        print("Нет данных")
        return
    else:
        data_vacancies = [formatter(row) for row in data_vacancies]

    if sort_string == "":
        pass
    elif sort_string == "Навыки":
        data_vacancies.sort(key=lambda d: len(d[sort_string].split("\n")),
                            reverse=convert_bool_reverse(reverse_sort))
    elif sort_string == "Оклад":
        data_vacancies.sort(key=lambda d: currency_dict[d['Оклад'][d['Оклад'].index('(') + 1:d['Оклад'].index(')')]] *
                                          (int(d[sort_string].replace(' ', '').split('-')[0]) +
                                           int(d[sort_string].replace(' ', '').split('-')[1]
                                               [:d[sort_string].replace(' ', '').split('-')[1].
                                               index('(')])) // 2,
                            reverse=convert_bool_reverse(reverse_sort))
    elif sort_string == "Опыт работы":
        data_vacancies.sort(key=lambda d: d[sort_string][3],
                            reverse=convert_bool_reverse(reverse_sort))
    else:
        data_vacancies.sort(key=lambda d: d[sort_string],
                            reverse=convert_bool_reverse(reverse_sort))

    for row in data_vacancies:
        row = {"№": count, **row}
        row['Дата публикации вакансии'] = get_date(row['Дата публикации вакансии'])
        vacancy_table.field_names = row.keys()
        if filter_string[0] == "" or (filter_string[0] in usual_tags and filter_string[1] == row[filter_string[0]]):
            vacancy_table.add_row(list(row_trim(row).values()))
            count += 1
        else:
            if filter_string[0] == "Навыки":
                if set(filter_string[1].split(", ")).issubset(row[filter_string[0]].split("\n")):
                    vacancy_table.add_row(list(row_trim(row).values()))
                    count += 1
            elif filter_string[0] == "Оклад":
                temp_string = row[filter_string[0]].replace(' ', '').split('-')
                if int(temp_string[0]) <= int(filter_string[1]) <= int(temp_string[1][:temp_string[1].index('(')]):
                    vacancy_table.add_row(list(row_trim(row).values()))
                    count += 1
            elif filter_string[0] == "Идентификатор валюты оклада":
                if row['Оклад'][row['Оклад'].index('(') + 1:row['Оклад'].index(')')] == filter_string[1]:
                    vacancy_table.add_row(list(row_trim(row).values()))
                    count += 1
        vacancy_table._max_width = {field: 20 for field in vacancy_table.field_names}

    if not numbers_none and not skills_none:
        numbers = numbers.split()
        if len(numbers) == 1:
            vacancy_table = vacancy_table.get_string(start=int(numbers[0]) - 1, fields=['№'] + skills.split(', '))
        else:
            vacancy_table = vacancy_table.get_string(start=int(numbers[0]) - 1, end=int(numbers[1]) - 1,
                                                     fields=['№'] + skills.split(', '))

    if not numbers_none and skills_none:
        numbers = numbers.split()
        if len(numbers) == 1:
            vacancy_table = vacancy_table.get_string(start=int(numbers[0]) - 1)
        else:
            vacancy_table = vacancy_table.get_string(start=int(numbers[0]) - 1, end=int(numbers[1]) - 1)

    if numbers_none and not skills_none:
        vacancy_table = vacancy_table.get_string(fields=['№'] + skills.split(', '))

    if count == 1:
        print("Ничего не найдено")
    else:
        print(vacancy_table)


keys = ["№", "Название", "Описание", "Навыки", "Опыт работы", "Премиум-вакансия", "Компания",
        "Оклад", "Название региона", "Дата публикации вакансии", "Идентификатор валюты оклада"]

file_name = input("Введите название файла: ")
filter_string = input("Введите параметр фильтрации: ")
sort_string = input("Введите параметр сортировки: ")
reverse_sort = input("Обратный порядок сортировки (Да / Нет): ")
numbers = input("Введите диапазон вывода: ")
skills = input("Введите требуемые столбцы: ")

if os.stat(file_name).st_size == 0:
    print("Пустой файл")
elif ':' not in filter_string and filter_string != "":
    print("Формат ввода некорректен")
elif filter_string.split(": ")[0] not in keys and filter_string.split(": ")[0] != "":
    print("Параметр поиска некорректен")
elif sort_string not in keys and sort_string != "":
    print("Параметр сортировки некорректен")
elif reverse_sort not in ["Да", "Нет", ""]:
    print("Порядок сортировки задан некорректно")
else:
    data = csv_reader(file_name)
    fix_data = csv_filer(data)
    print_vacancies(fix_data, filter_string, sort_string, reverse_sort, numbers, skills)