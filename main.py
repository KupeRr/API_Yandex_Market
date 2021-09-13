import yandex.loader as yandex
import cdek.loader as cdek
import boxberry.loader as boxberry

file    = ".config"
content = open(file).read()
config  = eval(content)

API_TOKEN_BOXBERRY      = config['API_TOKEN_BOXBERRY']

API_OAUTH_ID_YANDEX     = config['API_OAUTH_ID_YANDEX']
API_OAUTH_TOKEN_YANDEX  = config['API_OAUTH_TOKEN_YANDEX']
API_CAMPAIGN_ID_YANDEX  = config['API_CAMPAIGN_ID_YANDEX']


def print_choose_mode():
    print('='*100)
    print('Выберите режим работы:')
    print('(1) Загрузить ПВЗ конкретной зоны')
    print('(2) Загрузить ПВЗ конкретного города')
    try:
        mode = int(input('Введите номер желаемого режима: '))
    except ValueError:
        mode = -1

    if mode == 1:
        print('-'*100)
        print('Всего есть 3 зоны доставки.')
        
        return [int(input('Выберите номер зоны (от 1 до 3): '))]
    elif mode == 2:
        print('-'*100)
        print('Обратите внимание, что вводить наименования обязательно с большой буквы')
        print('Например: Город - Москва; Область -  Московская')
        print('-'*100)
        print('В случае если город относится не к области, а к республике:')
        print('Необходимо указать наименование республики в именительном падеже')
        print('Например: Город - Абакан; Республика - Хакасия')
        print('-'*100)

        city_name = input('Введите наименование города: ')
        city_area = input('Введите наименование области: ')

        if city_name == 'Москва': city_area = 'Москва'
        if city_name == 'Санкт-Петербург': city_area = 'Санкт-Петербург'

        return [[city_name], [city_area]]
    else:
        print('='*100)
        print('Вы ввели некорректно значение. Повторите ввод данных.')

        return print_choose_mode()


def print_choose_service():
    print('='*100)
    print('Выберите сервис доставки:')
    print('(1) CDEK')
    print('(2) Boxberrry')

    try:
        service_name = int(input('Введите номер желаемого сервиса доставки: '))
    except ValueError:
        service_name = -1

    if service_name == 1:
        return 'cdek'
    elif service_name == 2:
        return 'boxberry'
    else:
        print('='*100)
        print('Вы ввели некорректно значение. Повторите ввод данных.')

        return print_choose_service()


def get_correct_points(city_name, city_area, service_name, already_loaded_points, boxberry_token = API_TOKEN_BOXBERRY):
    print('='*100)
    print(f'Начинается загрузка ПВЗ из города [{city_name}] в области [{city_area}]')

    if service_name == 'cdek': 

        all_points_format_service_json = cdek.get_points_by_city(city_name, city_area)
        city_code = cdek.get_city_code(city_name, city_area)
        deliver_rule = cdek.get_rule_deliver_to_point(city_code)
        result = yandex.get_yandex_type(service_name, all_points_format_service_json, city_code, already_loaded_points, deliver_rule)

    elif service_name == 'boxberry': 

        all_points_format_service_json = boxberry.get_points_by_city(city_name, boxberry_token)
        city_code = boxberry.get_city_code(city_name, boxberry_token)
        result = yandex.get_yandex_type(service_name, all_points_format_service_json, city_code, already_loaded_points)

    print(f'Преобразовано {len(result)} к формату Яндекса')
    return result


def main():
    print('Запуск программы...')
    
    init_data = print_choose_mode()
    service_name = print_choose_service()

    already_loaded_points = yandex.get_all_points_yandex(API_CAMPAIGN_ID_YANDEX, API_OAUTH_TOKEN_YANDEX, API_OAUTH_ID_YANDEX)

    all_points_format_yandex_json = []

    if len(init_data) == 1:
        """
        If choosed load points by the zone number

        @todo Handle problem with area in zones
        """

        if      init_data[0] == 1: city_names = yandex.ZONE_1
        elif    init_data[0] == 2: city_names = yandex.ZONE_2
        elif    init_data[0] == 3: city_names = yandex.ZONE_3

        city_area = ''
        for city_name in city_names:
            all_points_format_yandex_json += get_correct_points(city_name, city_area, service_name, already_loaded_points)
            
    elif len(init_data) == 2:
        """
        If choosed load points by the city name
        """

        city_name = init_data[0][0]
        city_area = init_data[1][0]
        all_points_format_yandex_json += get_correct_points(city_name, city_area, service_name, already_loaded_points)

    
    if len(all_points_format_yandex_json) == 0: pass
    #yandex.upload_points_yandex(all_points_format_yandex_json, API_CAMPAIGN_ID_YANDEX, API_OAUTH_TOKEN_YANDEX, API_OAUTH_ID_YANDEX)

    print('/'*100)
    print(all_points_format_yandex_json)
    print('/'*100)

    print('Программа успешно завершила свою работу')
    #input('Нажмите Enter чтобы закрыть программу...')

if __name__ == '__main__':
    main()