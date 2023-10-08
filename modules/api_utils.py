from abc import ABC, abstractmethod
import requests
import json

API_SJ_KEY = 'v3.h.4538951.381a11dd65deabed4d7f551d13ed0afa9764f9b5.807be38b3cdfdb885fbde604be040efd1bdd4ab3'

class GetResponce(ABC):

    @abstractmethod
    def get_info(self):
        pass

# Класс для работы с сайтом ХэдХантер
class HH(GetResponce):
    def __init__(self, vacancies):

        self.vacancies = vacancies
        self.headers = {
            "User-Agent": "anonim_user"
        }
        self.params = {
            'text': self.vacancies,
            'per_page': 100,
            'code': "RUB",
            'only_with_salary': True,

        }
        self.responce = requests.get("https://api.hh.ru/vacancies", params=self.params, headers=self.headers)
        self.responce_json = self.responce.json()['items']

    def get_info(self):
        return self.make_json()

    def make_json(self):
        """Функция добавляет нужные названия ключей, для дальнейшего парсинга"""

        info = []
        for i in self.responce_json:
            i['payment_from'] = i['salary']['from']
            i['payment_to'] = i['salary']['to']
            i['currency']  = i['salary']['currency']
            info.append(i)
        return info

# Класс для работы с СуперДжоб
class SJ(GetResponce):

    def __init__(self, vacancies):
        self.vacancies = vacancies
        self.params = {
            'page:': 0,
            'count': 100,
            'keyword': self.vacancies
        }
        self.headers ={'X-Api-App-Id': API_SJ_KEY}

        self.responce = requests.get('https://api.superjob.ru/2.0/vacancies',headers=self.headers, params=self.params)
        self.responce_json = self.responce.json()['objects']

    def get_info(self):
        return self.make_json()


    def make_json(self):
        """Функция добавляет нужные названия ключей, для дальнейшего парсинга"""

        info = []
        for i in self.responce_json:
            i['name'] = i.pop('profession')
            i['alternate_url'] = i.pop('link')
            #i['salary'] = {'from': i['payment_from'], 'to': i['payment_to'], 'currency': i['currency']}
            i['snippet'] = {'requirement': i['candidat']}
            info.append(i)
        return info

class Vacancy:
    def __init__(self, vacancies):
        self.vacancies = vacancies

    def get_vac(self):
        """Функция парсит вакансии, предоставляя информацию пользователю"""

        chose_vac = []

        print('Список вакансий:')
        i = 0
        for vac in self.vacancies:
            i += 1
            title = vac['name']
            url = vac['alternate_url']
            payment_from = vac['payment_from']
            payment_to = vac['payment_to']
            requirements = vac['snippet']['requirement']
            if payment_from == None:
                payment_from = 'Не указана'
            if payment_to == None:
                payment_to = 'Не указана'

            print(f'{i}. {title}. Зарплата: от: {payment_from} до: {payment_to}. \n'
                  f' Требования: {requirements}\n'
                  f' Ссылка на вакансию: {url}')
            print()
        print('0: Выход')
        print()
        while True:
            """Пользователь выбирает вакансии, после чего сохраняет его выбор"""

            command = input('Выберите вакансию: ')
            if command == '0':
                return chose_vac
            else:
                if command.isdigit():
                    number = int(command)
                    if number > len(self.vacancies):
                        print('Такой вакансии нет')
                    else:
                        chose_vac.append(self.vacancies[number-1])
                else:
                    print('Введите номер вакансии')
