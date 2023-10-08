import json
from modules.api_utils import HH, SJ, Vacancy
from modules.json_utils import json_action

user_answer = input('Выберите профессию, по которой хотите искать вакансии: ')

def Main(vacancy = user_answer):
    with open('../saved_vacancies.json', 'r') as file:
        saved_vacancies = json.load(file)

    help_text = ('0: Выход\n'
                 '1: Показать вакансии HH\n'
                 '2: Показать вакансии SuperJob\n'
                 '3: Показать сохраненные вакансии (Обновляется после перезагрузки)\n'
                 '4: Загрузить выбранные вакансии в Файл\n'
                 '5: Выбрать и удалить вакансии из Файла'
                 )

    chosed_vacs = []
    print('welcome')
    info_HH = HH(vacancy).get_info()
    info_SJ = SJ(vacancy).get_info()
    while True:
        print(help_text)
        command = input('Введите команду: ')
        if command == '0':
            break

        elif command == '1':
            chosed_vacs.extend(Vacancy(info_HH).get_vac())
            print(chosed_vacs)

        elif command == '2':
            chosed_vacs.extend(Vacancy(info_SJ).get_vac())

        elif command == '3':
            for index, vac in enumerate(saved_vacancies):
                print(f'{index}. {saved_vacancies[index]["name"]} {saved_vacancies[index]["url"]}')

        elif command == '4':
            json_action(chosed_vacs).save_vac_to_db()

        elif command == '5':
            vac_to_del = int(input('Введите номер вакансии: '))
            json_action.del_vac_from_db(vac_to_del)


if __name__ == '__main__':
    Main()