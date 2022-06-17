import requests
import json
from typing import Dict, List, Any, Tuple, Union
from decouple import config
from loguru import logger
import traceback

KEY = config('KEY')

url = "https://hotels4.p.rapidapi.com/properties/list"

headers = {
    'x-rapidapi-host': "hotels4.p.rapidapi.com",
    'x-rapidapi-key': KEY
}


def price_hotels_request(destination_id: str, loc_lang: str, currency: str, check_in: str,
                         check_out: str, days_stay: int, sort_order: str) -> List[Dict[str, Any]]:
    """
    Hotel search function for lowprice and highprice
    :param destination_id: Destination ID
    :type: str
    :param loc_lang: Request language
    :type: str
    :param currency: Request currency
    :type: str
    :param check_in: Check in hotel
    :type: str
    :param check_out: Check out hotel
    :type: str
    :param days_stay: Days of stay
    :type: int
    :param sort_order: Sort order
    :type: str
    :return: List of Hotel Data Dictionaries
    :type: List[Dict[str, Any]
    """

    querystring = {"destinationId": destination_id, "pageNumber": "1", "pageSize": "25",
                   "checkIn": check_in, "checkOut": check_out, "adults1": "1",
                   "sortOrder": sort_order, "locale": loc_lang,
                   "currency": currency}

    try:
        response = requests.request('GET', url, headers=headers, params=querystring)

        found_hotels = json.loads(response.text)

        hotels_list = [{'name': hotel['name'],
                        'address': check_address(hotel),
                        'price': check_price(hotel, days_stay, loc_lang),
                        'hotel_id': str(hotel['id']),
                        'distance_center': hotel['landmarks'][0]['distance']}
                       for hotel in found_hotels['data']['body']['searchResults']['results']]

        return hotels_list

    except Exception as error:
        logger.error('error: {} \n{}', error, traceback.format_exc())

        hotels_list = []
        return hotels_list


def bestdeal_hotels_request(destination_id: str, loc_lang: str, currency: str, price_min: float,
                            price_max: float, page_number: int, check_in: str,
                            check_out: str, days_stay: int, sort_order: str) -> Tuple[List[Dict[str, Any]], Any]:
    """
    Hotel search function for bestdeal
    :param destination_id: Destination ID
    :type: str
    :param loc_lang: Request language
    :type: str
    :param currency: Request currency
    :type: str
    :param price_min: Min price
    :type: float
    :param price_max: Max price
    :type: float
    :param page_number: The page number in which data is display
    :type: int
    :param check_in: Check in hotel
    :type: str
    :param check_out: Check out hotel
    :type: str
    :param days_stay: Days of stay
    :type: int
    :param sort_order: Sort order
    :type: str
    :return: List of Hotel Data Dictionaries and total count
    :type: tuple[List[Dict[str, Any]], Any]
    """

    querystring = {"destinationId": destination_id, "pageNumber": page_number, "pageSize": "25",
                   "checkIn": check_in, "checkOut": check_out, "priceMin": price_min, "priceMax": price_max,
                   "sortOrder": sort_order, "locale": loc_lang, "currency": currency}

    try:
        response = requests.request('GET', url, headers=headers, params=querystring)

        found_hotels = json.loads(response.text)

        hotels_list = [{'name': hotel['name'],
                        'address': check_address(hotel),
                        'price': check_price(hotel, days_stay, loc_lang),
                        'hotel_id': str(hotel['id']),
                        'distance_center': hotel['landmarks'][0]['distance']}
                       for hotel in found_hotels['data']['body']['searchResults']['results']]

        total_count = found_hotels['data']['body']['searchResults']['totalCount']

        return hotels_list, total_count

    except Exception as error:
        logger.error('error: {} \n{}', error, traceback.format_exc())

        hotels_list = []
        total_count = 25

        return hotels_list, total_count


def check_address(address: Dict) -> str:
    """
    Checking for the presence of an address in the dictionary
    :param address: Dictionary address hotel
    :type: Dict
    :return: Address hotel
    :type: str
    """

    try:
        return address['address'].get('streetAddress', 'Адрес отсутсвует')

    except KeyError as error:
        logger.error('error: {} \n{}', error, traceback.format_exc())

        return 'Адрес отсутсвует'


def check_price(price: Dict, days_stay: int, loc_lang: str) -> Union[Tuple[int, int], Tuple[str, str]]:
    """
    Checking the presence of a price in the dictionary
    :param price: Dictionary price hotel
    :type: Dict
    :param days_stay: Days of stay
    :type: int
    :param loc_lang: Request language
    :type: str
    :return: Price hotel
    :type: Union[Tuple[int, int], Tuple[str, str]]
    """

    try:
        sum_price = int(price['ratePlan']['price'].get('exactCurrent', 'Цена отсутсвует'))

        if price['ratePlan']['price']['info'] and loc_lang == 'ru_RU':
            price_one_day = int(sum_price / days_stay)
            return price_one_day, sum_price
        else:
            raise KeyError('nightly price per room')

    except KeyError as error:
        logger.error('error: {} \n{}', error, traceback.format_exc())

        try:

            price_one_day = int(price['ratePlan']['price'].get('exactCurrent', 'Цена отсутсвует'))
            sum_price = int(price_one_day * days_stay)

            return price_one_day, sum_price

        except KeyError:
            return ('Цена отсутсвует', 'Цена отсутсвует')
