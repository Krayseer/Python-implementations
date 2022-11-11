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


job_title = input("Введите название вакансии: ")
job_description = input("Введите описание вакансии: ")
required_experience = int(input("Введите требуемый опыт работы (лет): "))
minimum_salary = int(input("Введите нижнюю границу оклада вакансии: "))
maximum_salary = int(input("Введите верхнюю границу оклада вакансии: "))
medium_salary = int((maximum_salary + minimum_salary) / 2)
is_free_schedule = input("Есть ли свободный график (да / нет): ")
is_premium_vacancy = input("Является ли данная вакансия премиум-вакансией (да / нет): ")


print(job_title)
print(f'Описание: {job_description}')
print(f'Требуемый опыт работы: {decline_value(required_experience, "year")}')
print(f'Средний оклад: {decline_value(medium_salary, "money")}')
print(f'Свободный график: {is_free_schedule}')
print(f'Премиум-вакансия: {is_premium_vacancy}')
