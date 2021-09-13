import requests

def get_city_code(city_name, token):
    """
    The city name function returns its ID from Boxberry

    @param city_name - The name of the city with a capital letter
    """

    URL_GET_CITIES = f'https://api.boxberry.ru/json.php?token={token}&method=ListCities&CountryCode=643'

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

def get_points_by_city(city_name, token):
    """
    The city ID function returns data on all delivery points from Boxberry

    @param city_code - city identifier
    """

    city_code = get_city_code(city_name, token)

    url = f'https://api.boxberry.ru/json.php?token={token}&method=ListPoints&prepaid=1&CityCode={city_code}&CountryCode=643'

    response = requests.request("GET", url).json()

    print(f'Получено {len(response)} элементов')
    return response