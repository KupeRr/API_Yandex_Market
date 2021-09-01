##########################################################################################################

####################################
###          Libraries           ###
####################################

import requests
import json

##########################################################################################################

####################################
###          Constants           ###
####################################

file    = ".config"
content = open(file).read()
config  = eval(content)

API_TOKEN_BOXBERRY      = config['API_TOKEN_BOXBERRY']
API_OAUTH_ID_YANDEX     = config['API_OAUTH_ID_YANDEX']
API_OAUTH_TOKEN_YANDEX  = config['API_OAUTH_TOKEN_YANDEX']
API_CAMPAIGN_ID_YANDEX  = config['API_CAMPAIGN_ID_YANDEX']
CITY_NAME               = config['CITY_NAME'].encode('cp1251').decode('utf-8')
ZONE_NUMBER             = int(config['ZONE_NUMBER'])

DELIVER_BOXBERRY_ID = 106

ZONE_1 = [  'Адлер', 'Альметьевск', 'Арзамас', 'Астрахань', 'Батайск', 'Белгород', 'Бердск', 'Брянск', 'Великий Новгород', 'Владимир', 
            'Волгоград', 'Волжский', 'Воронеж', 'Дзержинск', 'Димитровград', 'Екатеринбург', 'Елец', 'Железногорск', 'Иваново', 'Ижевск', 
            'Йошкар-Ола', 'Казань', 'Калуга', 'Каменск-Уральский', 'Киров', 'Ковров', 'Колпино', 'Копейск', 'Кострома', 'Краснодар', 
            'Красноярск', 'Курск', 'Липецк', 'Миасс', 'Москва', 'Московская область', 'Набережные Челны', 'Нижнекамск', 'Нижний Новгород', 
            'Новокуйбышевск', 'Новомосковск', 'Новороссийск', 'Новосибирск', 'Новочебоксарск', 'Новочеркасск', 'Новошахтинск', 'Обнинск', 
            'Омск', 'Орёл', 'Оренбург', 'Пенза', 'Первоуральск', 'Пермь', 'Пушкин', 'Ростов-на-Дону', 'Рыбинск', 'Рязань', 'Самара', 
            'Санкт-Петербург', 'Саратов', 'Смоленск', 'Сочи', 'Сызрань', 'Таганрог', 'Тамбов', 'Тверь', 'Тольятти', 'Тула', 'Тюмень', 
            'Ульяновск', 'Уфа', 'Чебоксары', 'Челябинск', 'Шахты', 'Энгельс', 'Ярославль']

ZONE_2 = [  'Абакан', 'Ангарск', 'Армавир', 'Архангельск', 'Ачинск', 'Балаково', 'Барнаул', 'Березники', 'Бийск', 'Владикавказ', 'Волгодонск', 
            'Вологда', 'Грозный', 'Дербент', 'Евпатория', 'Ессентуки', 'Златоуст', 'Иркутск', 'Калининград', 'Камышин', 'Каспийск', 'Кемерово', 
            'Керчь', 'Кисловодск', 'Курган', 'Кызыл', 'Магнитогорск', 'Майкоп', 'Махачкала', 'Мурманск', 'Муром', 'Назрань', 'Нальчик', 
            'Невинномысск', 'Нефтекамск', 'Нефтеюганск', 'Нижневартовск', 'Нижний Тагил', 'Новокузнецк', 'Октябрьский', 'Орск', 'Петрозаводск', 
            'Прокопьевск', 'Псков', 'Пятигорск', 'Рубцовск', 'Салават', 'Саранск', 'Севастополь', 'Северодвинск', 'Северск', 'Симферополь', 
            'Ставрополь', 'Старый Оскол', 'Стерлитамак', 'Сургут', 'Сыктывкар', 'Тобольск', 'Томск', 'Улан-Удэ', 'Череповец', 'Черкесск', 'Элиста']

ZONE_3 = [  'Артём', 'Благовещенск', 'Братск', 'Владивосток', 'Комсомольск-на-Амуре', 'Находка', 'Новый Уренгой', 'Норильск', 'Ноябрьск', 
            'Петропавловск-Камчатский', 'Уссурийск', 'Хабаровск', 'Хасавюрт', 'Чита', 'Южно-Сахалинск', 'Якутск']


##########################################################################################################

#####################################################
###          Functions for Boxberry API           ###
#####################################################


def get_boxberry_city_code(city_name):
    """
    The city name function returns its ID from Boxberry

    @param city_name - The name of the city with a capital letter
    """

    URL_GET_CITIES = f'https://api.boxberry.ru/json.php?token={API_TOKEN_BOXBERRY}&method=ListCities&CountryCode=643'

    all_cities = {}

    response = requests.request('GET', URL_GET_CITIES)

    for item in response.json():
        all_cities[item['Name']] = item['Code']

    try:
        return all_cities[city_name]
    except KeyError:
        print(f'В Boxberry отсутствуют точки в городе [{city_name}]')
        print('=' * 100)
        return -1


def get_boxberry_city_data(city_code):
    """
    The city ID function returns data on all delivery points from Boxberry

    @param city_code - city identifier
    """

    url = f'https://api.boxberry.ru/json.php?token={API_TOKEN_BOXBERRY}&method=ListPoints&prepaid=1&CityCode={city_code}&CountryCode=643'

    response = requests.request("GET", url)

    return response.json()


##########################################################################################################

###################################################
###          Functions for Yandex API           ###
###################################################


def get_all_points_yandex():
    """
    The function returns the names of all existing delivery points from the current campaign in Yandex
    """

    url = f'https://api.partner.market.yandex.ru/v2/campaigns/{API_CAMPAIGN_ID_YANDEX}/outlets.json'

    headers = {
        'Authorization': f'OAuth oauth_token={API_OAUTH_TOKEN_YANDEX}, oauth_client_id={API_OAUTH_ID_YANDEX}',
        'Content-Type' : 'application/json'
    }
    data = requests.request("GET", url, headers=headers).json()

    result = set()
    for item in data['outlets']:
        result.add(item['name'])
    
    return result


def get_shedule_items(shedule_box):
    """
    The function converts the delivery point schedule from Boxberry format to Yandex format

    @param shedule_box - The line that contains information about the schedule
    """

    if(len(shedule_box) == 0): return -1

    while shedule_box.find(',') != -1:
        first_ind = shedule_box.find(',')
        shedule_box = shedule_box[:first_ind] + shedule_box[first_ind + 19:]

    shedule = []
    for item in (shedule_box[0 + i : 16 + i] for i in range(0, len(shedule_box), 16)):
        if get_format_day(item[:2]) == -1: return -1

        buff = item.split(' ')
        shedule.append([buff[0], buff[1]])

    result = []
    for item in shedule:
        same_time_shedule = False
        for item_result in result:
            if item_result['startTime'] == item[1].split('-')[0] and item_result['endTime'] == item[1].split('-')[1]:
                item_result['endDay'] = get_format_day(item[0][:-1])
                same_time_shedule = True
        
        if same_time_shedule: continue

        result.append({
            'startDay'  : get_format_day(item[0][:-1]),
            'endDay'    : get_format_day(item[0][:-1]),
            'startTime' : item[1].split('-')[0],
            'endTime'   : item[1].split('-')[1]
        })

    return result


def get_format_day(day_of_week):
    """
    The function converts the day of the week from the Boxberry standard to the Yandex standard

    @param day_of_week - value of current day
    """

    if day_of_week == 'пн':
        return 'MONDAY'
    elif day_of_week == 'вт':
        return 'TUESDAY'
    elif day_of_week == 'ср':
        return 'WEDNESDAY'
    elif day_of_week == 'чт':
        return 'THURSDAY'
    elif day_of_week == 'пт':
        return 'FRIDAY'
    elif day_of_week == 'сб':
        return 'SATURDAY'
    elif day_of_week == 'вс':
        return 'SUNDAY'
    return -1


def get_format_phone(phone_number):
    """
    The function converts the phone number from the Boxberry standard to the Yandex standard

    @param phone_number - phone number in Boxberry standart
    """

    try:
        if phone_number[1] == '-':
            return f'+{phone_number[0]} ({phone_number[2:5]}) {phone_number[6:]}'
        return f'{phone_number[:2]} {phone_number[2:7]} {phone_number[7:]}'
    except IndexError:
        return -1


def get_yandex_type(json, city_code, already_loads_points):
    """
    The function converts the data received from Boxberry to Yandex format
    It also checks if the current delivery point already exists in the Yandex campaign

    @param json                 - data from Boxberry
    @param city_code            - city ID from Yandex
    @param already_loads_points - Delivery points already added to Yandex
    """

    all_items = []
    for item in json:
        if item['Name'] in already_loads_points: 
            print(f"ПВЗ с именем {item['Name']} уже загружена.")
            continue

        type = 'DEPOT'
        if item['TypeOfOffice'] == 'СПВЗ':
            type = 'MIXED'

        sheduleItems = get_shedule_items(item['WorkShedule'])

        if len(item['AddressReduce']) == 0: continue
        elif sheduleItems == -1: continue

        rule = []
        rule.append({
            'cost'              : float(0),
            'minDeliveryDays'   : int(item['DeliveryPeriod']),
            'maxDeliveryDays'   : int(item['DeliveryPeriod']),
            'deliveryServiceId' : int(DELIVER_BOXBERRY_ID)
        })

        phone_number = get_format_phone(item['Phone'])
        if phone_number == -1: continue

        all_items.append({
            'name'              : item['Name'],
            'type'              : type,
            'coords'            : item['GPS'],
            'address'           : {
                'regionId'          : city_code,
                'street'            : item['AddressReduce'].split(',')[0],
                'number'            : item['AddressReduce'].split(',')[1],
                'additional'        : item['TripDescription']
            },
            'phones'            : [phone_number],
            'workingSchedule'   : {
                'scheduleItems'     : sheduleItems,
            },
            'deliveryRules'     : rule,
        })

    return all_items


def upload_point_yandex(data):
    """
    The function uploads data about delivery points to Yandex

    @param data - data about delivery points
    """

    url = f'https://api.partner.market.yandex.ru/v2/campaigns/{API_CAMPAIGN_ID_YANDEX}/outlets.json'

    headers = {
        'Authorization': f'OAuth oauth_token={API_OAUTH_TOKEN_YANDEX}, oauth_client_id={API_OAUTH_ID_YANDEX}',
        'Content-Type' : 'application/json'
    }

    for i in range(len(data)):
        response = requests.request("POST", url, headers=headers, data=json.dumps(data[i]))
        print(f"Загружена {i+1} точка под названием: [{data[i]['name']}]")
    
    if response.json()['status'] != 'OK': print('Error in request under this msg...')


def get_city_code_yandex(name):
    """
    The function returns the city ID by its name from the Yandex API

    @param name - city name
    """

    url = f'https://api.partner.market.yandex.ru/v2/regions.json?name={name}'

    headers = {
        'Authorization': f'OAuth oauth_token={API_OAUTH_TOKEN_YANDEX}, oauth_client_id={API_OAUTH_ID_YANDEX}',
        'Content-Type' : 'application/json'
    }
    data = requests.request("GET", url, headers=headers).json()
    
    return data['regions'][0]['id']


##########################################################################################################

#########################################
###          Main functions           ###
#########################################


def load_all_points(all_zones = [CITY_NAME]):
    """
    The function loads all delivery points in the list of cities or a specific city from Boxberry 
    and uploads the data of each point to the campaign in Yandex

    @param all_zones - list of cities
    """

    print('Запуск...')

    already_loads_points = get_all_points_yandex()

    for city_name in all_zones:
        print(f'Начинается загрузка ПВЗ из города: [{city_name}]')
        city_code = get_boxberry_city_code(city_name)
        if city_code == -1: continue

        print('Получение данных из Boxberry...')
        data = get_boxberry_city_data(city_code)
        print(f'Получено {len(data)} элементов')

        city_code_yndx = int(get_city_code_yandex(city_name))

        print('Преобразование элементов к формату Яндекса...')
        all_items = get_yandex_type(data, city_code_yndx, already_loads_points)
        print(f'Преобразовано {len(all_items)}. {len(data) - len(all_items)} элементов были записаны в Boxberry некорректно.')

        print('Начало загрузки ПВЗ в Яндекс...')
        upload_point_yandex(all_items)
        
        print('=' * 100)

    print('Все ПВЗ загружены.')


def main():
    if   ZONE_NUMBER == 1: load_all_points(all_zones=ZONE_1)
    elif ZONE_NUMBER == 2: load_all_points(all_zones=ZONE_2)
    elif ZONE_NUMBER == 3: load_all_points(all_zones=ZONE_3)
    else:                  load_all_points()


if __name__ == '__main__':
    main()

