def decline_value(number, value):
    number = str(number)
    word = ""

    if int(number[-1]) >= 5 or (int(number[0]) == 1 and len(number) > 1):
        word = " лет" if value == "year" else " рублей"
    elif 2 <= int(number[-1]) <= 4:
        word = " года" if value == "year" else " рубля"
    elif int(number[-1]) == 1:
        word = " год" if value == "year" else " рубль"

    return number + word


while True:
    job_title = input("Введите название вакансии: ")
    if len(job_title.strip()) == 0:
        print("Данные некорректны, повторите ввод")
    else:
        break

while True:
    job_description = input("Введите описание вакансии: ")
    if len(job_description.strip()) == 0:
        print("Данные некорректны, повторите ввод")
    else:
        break

while True:
    required_experience = input("Введите требуемый опыт работы (лет): ")
    if not(required_experience.isdigit()) or len(required_experience.strip()) == 0:
        print("Данные некорректны, повторите ввод")
    else:
        break

while True:
    minimum_salary = input("Введите нижнюю границу оклада вакансии: ")
    if not(minimum_salary.isdigit()) or len(minimum_salary.strip()) == 0:
        print("Данные некорректны, повторите ввод")
    else:
        break

while True:
    maximum_salary = input("Введите верхнюю границу оклада вакансии: ")
    if not(maximum_salary.isdigit()) or len(maximum_salary.strip()) == 0:
        print("Данные некорректны, повторите ввод")
    else:
        break

medium_salary = int((int(maximum_salary) + int(minimum_salary)) / 2)

while True:
    is_free_schedule = input("Есть ли свободный график (да / нет): ")
    if is_free_schedule != "да" and is_free_schedule != "нет" or len(is_free_schedule.strip()) == 0:
        print("Данные некорректны, повторите ввод")
    else:
        break

while True:
    is_premium_vacancy = input("Является ли данная вакансия премиум-вакансией (да / нет): ")
    if is_premium_vacancy != "да" and is_premium_vacancy != "нет" or len(is_premium_vacancy.strip()) == 0:
        print("Данные некорректны, повторите ввод")
    else:
        break

print(job_title)
print(f'Описание: {job_description}')
print(f'Требуемый опыт работы: {decline_value(required_experience, "year")}')
print(f'Средний оклад: {decline_value(medium_salary, "money")}')
print(f'Свободный график: {is_free_schedule}')
print(f'Премиум-вакансия: {is_premium_vacancy}')
