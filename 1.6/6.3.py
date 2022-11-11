import csv


class DataSet:
    def __init__(self):
        self.file_name = input("Введите название файла: ")
        self.profession_name = input("Введите название профессии: ")
        currency_name = ["AZN", "BYR", "EUR", "GEL", "KGS", "KZT", "RUR", "UAH", "USD", "UZS"]
        currency_value = [35.68, 23.91, 59.90, 21.74, 0.76, 0.13, 1, 1.64, 60.66, 0.0055]
        self.currency_to_rub = dict(zip(currency_name, currency_value))
        self.professions = []

    def get_correct_data(self):
        with open(self.file_name, encoding='utf-8-sig') as file:
            for row in csv.DictReader(file):
                correct_row = True
                for field in row:
                    if row[field] is None or len(row[field]) == 0:
                        correct_row = False
                        continue
                if correct_row:
                    self.professions.append(Profession(*[row[field] for field in row]))

    def get_info(self):
        salary_dict = dict()
        count_dict = dict()
        for profession in self.professions:
            profession.salary_from = int(str(profession.salary_from).replace('.0', ''))
            profession.salary_to = int(str(profession.salary_to).replace('.0', ''))
            if profession.get_year() not in salary_dict.keys():
                salary_dict[profession.get_year()] = []
            salary_dict[profession.get_year()].append((profession.salary_from + profession.salary_to) // 2
                                                      * self.currency_to_rub[profession.salary_currency])
        for key, value in salary_dict.items():
            salary_dict[key] = int(str((sum(value) // len(value))).replace('.0', ''))
            count_dict[key] = len(value)
        print("Динамика уровня зарплат по годам:", salary_dict)
        print('Динамика количества вакансий по годам:', count_dict)

    def get_info_professions(self):
        salary_dict = dict()
        count_dict = dict()
        for profession in self.professions:
            if profession.get_year() not in salary_dict.keys():
                salary_dict[profession.get_year()] = []
            if self.profession_name in profession.name:
                profession.salary_from = int(str(profession.salary_from).replace('.0', ''))
                profession.salary_to = int(str(profession.salary_to).replace('.0', ''))
                salary_dict[profession.get_year()].append((profession.salary_from + profession.salary_to) // 2
                                                          * self.currency_to_rub[profession.salary_currency])
        for key, value in salary_dict.items():
            if len(value) != 0:
                salary_dict[key] = int(str((sum(value) // len(value))).replace('.0', ''))
                count_dict[key] = len(value)
            else:
                salary_dict[key] = 0
                count_dict[key] = 0

        print("Динамика уровня зарплат по годам для выбранной профессии:", salary_dict)
        print('Динамика количества вакансий по годам для выбранной профессии:', count_dict)

    def get_info_cities(self):
        city_dict = dict()
        ans_dict = dict()
        count_vacancy = 0
        for profession in self.professions:
            profession.salary_from = int(str(profession.salary_from).replace('.0', ''))
            profession.salary_to = int(str(profession.salary_to).replace('.0', ''))
            if profession.area_name not in city_dict.keys():
                city_dict[profession.area_name] = []
            city_dict[profession.area_name].append((profession.salary_from + profession.salary_to) // 2
                                                   * self.currency_to_rub[profession.salary_currency])
            count_vacancy += 1
        percent_dict = dict()
        for key, value in city_dict.items():
            if len(value) >= count_vacancy // 100:
                ans_dict[key] = int(str((sum(value) // len(value))).replace('.0', ''))
                percent_dict[key] = round(len(value) / count_vacancy, 4)
        ans_dict = dict(sorted(ans_dict.items(), key=lambda item: item[1], reverse=True)[:10])
        percent_dict = dict(sorted(percent_dict.items(), key=lambda item: item[1], reverse=True)[:10])
        print('Уровень зарплат по городам (в порядке убывания):', ans_dict)
        print('Доля вакансий по городам (в порядке убывания):', percent_dict)


class Profession:
    def __init__(self, name, salary_from, salary_to, salary_currency, area_name, published_at):
        self.name = name
        self.salary_from = int(salary_from.replace('.0', ''))
        self.salary_to = int(salary_to.replace('.0', ''))
        self.salary_currency = salary_currency
        self.area_name = area_name
        self.published_at = published_at

    def get_year(self):
        return self.published_at[:4]


data_professions = DataSet()
data_professions.get_correct_data()
data_professions.get_info()
data_professions.get_info_professions()
data_professions.get_info_cities()
