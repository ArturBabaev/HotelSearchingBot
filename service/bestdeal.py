from botrequests.hotels_req import bestdeal_hotels_request
from typing import Dict, List, Any, Tuple, Union
from math import ceil


def bestdeal_hotels(destination_id: str, loc_lang: str, currency: str, hotels_qty: int, distance_min: float,
                    distance_max: float, price_min: int, price_max: int, check_in: str, check_out: str,
                    days_stay: int, page_number: int, bestdeal_hotels_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Sort hotels by distance from center and price
    :param destination_id: Destination ID
    :type: str
    :param loc_lang: Request language
    :type: str
    :param currency: Request currency
    :type: str
    :param hotels_qty: Hotels qty
    :type: int
    :param distance_min: Distance min
    :type: float
    :param distance_max: Distance max
    :type: float
    :param price_min: Price min
    :type: int
    :param price_max: Price max
    :type: int
    :param check_in: Check in hotel
    :type: str
    :param check_out: Check out hotel
    :type: str
    :param days_stay: Days of stay
    :type: int
    :param page_number: Page number
    :type: int
    :param bestdeal_hotels_list: List of Hotel Data Dictionaries
    :type: List[Dict[str, Any]]
    :return: List of Hotel Data Dictionaries
    :type: List[Dict[str, Any]]
    """

    distance_max, distance_min = change_values(distance_max, distance_min)
    price_max, price_min = change_values(price_max, price_min)

    hotels_list = bestdeal_hotels_request(destination_id, loc_lang, currency, price_min, price_max, page_number,
                                          check_in, check_out, days_stay, sort_order='DISTANCE_FROM_LANDMARK')

    filter_hotels_list = filter(
        lambda elem: distance_min <= str_to_float(elem['distance_center']) <= distance_max, hotels_list[0])

    bestdeal_hotels_list.extend(filter_hotels_list)

    pages_number = ceil(hotels_list[1] / 25)

    if len(bestdeal_hotels_list) >= hotels_qty:
        return bestdeal_hotels_list[:hotels_qty]
    elif len(bestdeal_hotels_list) < hotels_qty:
        page_number += 1
        if page_number < pages_number:
            return bestdeal_hotels(destination_id, loc_lang, currency, hotels_qty, distance_min,
                                   distance_max, price_min, price_max, check_in, check_out,
                                   days_stay, page_number, bestdeal_hotels_list)
        elif page_number == pages_number:
            return bestdeal_hotels_list


def str_to_float(string: str) -> float:
    """
    String conversion an float
    :param string: String
    :type: str
    :return: Floating point number
    :type: float
    """

    split_str = string.split(' ')
    replace_str = float(split_str[0].replace(',', '.'))
    return replace_str


def change_values(max_val: Union[float, int], min_val: Union[float, int]) -> Union[Tuple[float, float], Tuple[int, int]]:
    """
    Change values function
    :param max_val: Maximum value
    :type: float
    :param min_val: Minimum value
    :type: float
    :return: Maximum and minimum value
    :type: tuple[float, float]
    """

    if min_val > max_val:
        max_val, min_val = min_val, max_val
    return max_val, min_val
