import requests


API_TOKEN_BOXBERRY  = '1'
API_ID_YANDEX       = '11-'
API_TOKEN_YANDEX    = '2'


def get_city_code(city_name):

    URL_GET_CITIES = f'https://api.boxberry.ru/json.php?token={API_TOKEN_BOXBERRY}&method=ListCities&CountryCode=643'

    all_cities = {}

    response = requests.request('GET', URL_GET_CITIES)

    for item in response.json():
        all_cities[item['Name']] = item['Code']

    return all_cities[city_name]


def get_city_data(city_code):

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
    #print(f'WRONG FORMAT -> {str}')
    return -1
    


def get_yndx_type(json, deliver_id): #deliver_id???
    all_items = []
    for item in json:
        type = 'DEPOT'
        if item['TypeOfOffice'] == 'СПВЗ':
            type = 'MIXED'

        coords = item['GPS'].split(',')

        sheduleItems = get_shedule_items(item['WorkShedule'])
        
        if len(item['AddressReduce']) == 0: continue
        elif sheduleItems == -1: continue

        all_items.append({
            'name'              : item['Name'],
            'type'              : type,
            'coords'            : ', '.join([coords[0], coords[1]]),
            'address'           : {
                'regionId'          : item['CityCode'],
                'street'            : item['AddressReduce'].split(',')[0],
                'number'            : item['AddressReduce'].split(',')[1],
                'additional'        : item['TripDescription']
            },
            'phones'            : [item['Phone']],
            'workingSchedule'   : {
                'scheduleItems'     : sheduleItems,
            },
            'deliveryRules'     : {
                'cost'              : 0,
                'minDeliveryDays'   : item['DeliveryPeriod'],
                'minDeliveryDays'   : item['DeliveryPeriod'],
                'deliveryServiceId' : deliver_id
            },
        })

    return all_items



name = 'Москва'
"""
city_code = get_city_code(name)
data = get_city_data(city_code)
all_items = get_yndx_type(data, 123)
"""

url = f'https://api.partner.market.yandex.ru/v2/campaigns.json'
headers = {
    'Authorization':f'OAuth oauth_token={API_TOKEN_YANDEX}, oauth_client_id={API_ID_YANDEX}'
}
print()
response = requests.request("GET", url, headers=headers)
print(response.json())
