from os import PathLike
import requests
import json
import codecs

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

ZONE_1 = ['Адлер', 'Арзамас', 'Ижевск', 'Уфа', 'Сызрань', 'Киров', 'Самара', 'Орёл', 'Орел']
ZONE_2 = ['Зона_2']
ZONE_3 = ['Зона_3']

def get_boxberry_city_code(city_name):

    URL_GET_CITIES = f'https://api.boxberry.ru/json.php?token={API_TOKEN_BOXBERRY}&method=ListCities&CountryCode=643'

    all_cities = {}

    response = requests.request('GET', URL_GET_CITIES)

    for item in response.json():
        all_cities[item['Name']] = item['Code']

    try:
        return all_cities[city_name]
    except KeyError:
        print(f'В Boxberry отсутствуют точки в городе {city_name}')
        print('=' * 100)
        return -1


def get_boxberry_city_data(city_code):

    url = f'https://api.boxberry.ru/json.php?token={API_TOKEN_BOXBERRY}&method=ListPoints&prepaid=1&CityCode={city_code}&CountryCode=643'

    response = requests.request("GET", url)

    return response.json()

def get_shedule_items(shedule_box):
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

def get_format_day(str):
    if str == 'пн':
        return 'MONDAY'
    elif str == 'вт':
        return 'TUESDAY'
    elif str == 'ср':
        return 'WEDNESDAY'
    elif str == 'чт':
        return 'THURSDAY'
    elif str == 'пт':
        return 'FRIDAY'
    elif str == 'сб':
        return 'SATURDAY'
    elif str == 'вс':
        return 'SUNDAY'
    return -1
    
def get_format_phone(str):
    if str[1] == '-':
        return f'+{str[0]} ({str[2:5]}) {str[6:]}'
    return f'{str[:2]} {str[2:7]} {str[7:]}'

def get_yandex_type(json, city_code):
    all_items = []
    for item in json:
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
            'phones'            : [get_format_phone(item['Phone'])],
            'workingSchedule'   : {
                'scheduleItems'     : sheduleItems,
            },
            'deliveryRules'     : rule,
        })

    return all_items


def upload_point_yandex(items):
    url = f'https://api.partner.market.yandex.ru/v2/campaigns/{API_CAMPAIGN_ID_YANDEX}/outlets.json'

    headers = {
        'Authorization': f'OAuth oauth_token={API_OAUTH_TOKEN_YANDEX}, oauth_client_id={API_OAUTH_ID_YANDEX}',
        'Content-Type' : 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(items[0]))
    if response.json()['status'] != 'OK': print('Error in request under this msg...')

def delete_point(num): ###################
    url = f'https://api.partner.market.yandex.ru/v2/campaigns/{API_CAMPAIGN_ID_YANDEX}/outlets/{num}.json'

    headers = {
        'Authorization': f'OAuth oauth_token={API_OAUTH_TOKEN_YANDEX}, oauth_client_id={API_OAUTH_ID_YANDEX}',
        'Content-Type' : 'application/json'
    }
    response = requests.request("DELETE", url, headers=headers)
    print(response.json())

def get_city_code_yandex(name):
    url = f'https://api.partner.market.yandex.ru/v2/regions.json?name={name}'

    headers = {
        'Authorization': f'OAuth oauth_token={API_OAUTH_TOKEN_YANDEX}, oauth_client_id={API_OAUTH_ID_YANDEX}',
        'Content-Type' : 'application/json'
    }
    data = requests.request("GET", url, headers=headers).json()
    
    return data['regions'][0]['id']

def load_all_points(all_zones = [CITY_NAME]):
    print('Запуск...')

    for city_name in all_zones:
        print(f'Начинается загрузка ПВЗ из города: {city_name}')
        city_code = get_boxberry_city_code(city_name)
        if city_code == -1: continue

        print('Получение данных из Boxberry...')
        data = get_boxberry_city_data(city_code)
        print(f'Получено {len(data)} элементов')

        city_code_yndx = int(get_city_code_yandex(city_name))

        print('Преобразование элементов к формату Яндекса...')
        all_items = get_yandex_type(data, city_code_yndx)
        print(f'Преобразовано {len(all_items)}. {len(data) - len(all_items)} элементов были записаны в Boxberry некорректно.')

        print('Начало загрузки ПВЗ в Яндекс...')
        for i in range(1): ##########
            upload_point_yandex([all_items[i]])
            print(f"Загружена {i+1} точка под названием: {all_items[i]['name']}")
        
        print('=' * 100)

    print('Все ПВЗ загружены.')

def main():
    #for i in range(328968832, 328968836):
    #    delete_point(i)

    if   ZONE_NUMBER == 1: load_all_points(all_zones=ZONE_1)
    elif ZONE_NUMBER == 2: load_all_points(all_zones=ZONE_2)
    elif ZONE_NUMBER == 3: load_all_points(all_zones=ZONE_3)
    else:                  load_all_points()
    


if __name__ == '__main__':
    main()

