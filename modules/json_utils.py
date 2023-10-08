from abc import ABC, abstractmethod
import json

class JSON_Options(ABC):
    def save_vac_to_db(self):
        pass
    def del_vac_from_db(to_del):
        pass

class json_action(JSON_Options):

    def __init__(self, vacancies):
        self.vacancies = vacancies

    def save_vac_to_db(self):
        """Функция согхраняет данные в Файл."""

        for index, vac in enumerate(self.vacancies):
            json_data = {
                'name': self.vacancies[index]['name'],
                'url': self.vacancies[index]['alternate_url'],
            }
            data = json.load(open('../saved_vacancies.json'))
            data.append(json_data)
            with open('../saved_vacancies.json', 'w') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)

    @staticmethod
    def del_vac_from_db(to_del):
        """Функция принимает индекс элемента который нужно удалить из файла,
        после чего удаляет вакансию"""

        with open('../saved_vacancies.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            minimal = 0
            for i in data:
                if data.index(i) == to_del:
                    data.pop(minimal)
                elif data.index(i) > len(data):
                    print('Таких вакансий нет!')
                minimal += 1

            with open('../saved_vacancies.json', 'w', encoding='utf-8') as out:
                json.dump(data, out, ensure_ascii=False, indent=2)