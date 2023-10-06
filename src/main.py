import json
from  modules.api_utils import HH, SJ, Parser
from modules.json_utils import json_action

class Main:

    def __init__(self):
        self.get_vac_from_db()
        self.chosed_vacs = []

    def __call__(self, *args, **kwargs):
        print("Добро пожаловать!")
        user_answer = input('Выберите профессию, по которой хотите искать вакансии: ')
        info_HH = HH(user_answer).get_info()
        info_SJ = SJ(user_answer).get_info()
        while True:
            self._help_text()
            command = input('Введите команду: ')
            if command == '0':

                break
            elif command == '1':
                self.chosed_vacs.extend(Parser(info_HH).get_vac())

            elif command == '2':
                self.chosed_vacs.extend(Parser(info_SJ).get_vac())

            elif command == '3':
                for index, vac in enumerate(self.saved_vacancies):
                    print(f'{index}. {self.saved_vacancies[index]["name"]} {self.saved_vacancies[index]["url"]}')

            elif command == '4':
                json_action(self.chosed_vacs).save_vac_to_db()

            elif command == '5':
                vac_to_del = int(input('Введите номер вакансии: '))
                json_action.del_vac_from_db(vac_to_del)


    def _help_text(self):
        print("Доступные команды:")
        print('0: Выход')
        print('1: Показать вакансии HH')
        print('2: Показать вакансии SuperJob')
        print('3: Показать сохраненные вакансии (Обновляется после перезагрузки)')
        print('4: Загрузить выбранные вакансии в Файл')
        print('5: Выбрать и удалить вакансии из Файла')

    def get_vac_from_db(self):
        """Функция загружает вакансии из Файла"""

        with open('../saved_vacancies.json', 'r') as file:
            self.saved_vacancies = json.load(file)

if __name__ == '__main__':
    main = Main()
    main()