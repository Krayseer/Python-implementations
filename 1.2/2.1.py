def convert_bool(value):
    if value == "да":
        return True
    return False


job_title = input("Введите название вакансии: ")
job_description = input("Введите описание вакансии: ")
required_experience = int(input("Введите требуемый опыт работы (лет): "))
minimum_salary = int(input("Введите нижнюю границу оклада вакансии: "))
maximum_salary = int(input("Введите верхнюю границу оклада вакансии: "))
is_free_schedule = convert_bool(input("Есть ли свободный график (да / нет): "))
is_premium_vacancy = convert_bool(input("Является ли данная вакансия премиум-вакансией (да / нет): "))


print(f'{job_title} ({type(job_title).__name__})')
print(f'{job_description} ({type(job_description).__name__})')
print(f'{required_experience} ({type(required_experience).__name__})')
print(f'{minimum_salary} ({type(minimum_salary).__name__})')
print(f'{maximum_salary} ({type(maximum_salary).__name__})')
print(f'{is_free_schedule} ({type(is_free_schedule).__name__})')
print(f'{is_premium_vacancy} ({type(is_premium_vacancy).__name__})')