import requests
import json

__DELIVER_CDEK_ID = 51

def get_points_by_city(name, area):
    url = f'http://integration.cdek.ru/pvzlist/v1/json?cityid={get_city_code(name, area)}'

    response = requests.request("GET", url).json()

    print(f"Получено {len(response['pvz'])} элементов")
    return response['pvz']


def get_rule_deliver_to_point(code):
    url = f'http://api.cdek.ru/calculator/calculate_price_by_json.php'

    headers = {
        'Content-Type' : 'application/json'
    }

    info = {
        "version"           : "1.0",
        "senderCityId"      : get_city_code('Москва', 'Москва'),
        "receiverCityId"    : code,
        "tariffId"          : 363,
        "goods" :
            [
                {
                    "weight"    : "0.2",
                    "length"    : "20",
                    "width"     : "30",
                    "height"    : "10"
                }
            ],
    }  
    response = requests.request("POST", url, headers=headers, data=json.dumps(info)).json()

    try:
        data = response['result']
    except KeyError:
        return {'cost':-1}

    return {
        'cost'              : data['price'],
        'minDeliveryDays'   : data['deliveryPeriodMin'],
        'maxDeliveryDays'   : data['deliveryPeriodMax'],
        'deliveryServiceId' : __DELIVER_CDEK_ID
    }


def get_city_code(name, area):
    url = f'http://integration.cdek.ru/v1/location/cities/json?cityName={name}'

    response = requests.request("GET", url).json()

    if len(response) == 1 or area == '': return response[0]['cityCode']
    
    for item in response:
        try:
            if item['region'].split()[0] == area: return item['cityCode']
        except KeyError:
            return item['cityCode']