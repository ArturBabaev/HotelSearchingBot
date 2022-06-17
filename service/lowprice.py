from botrequests.hotels_req import price_hotels_request
from typing import Dict, List, Any


def lowprice_hotels(destination_id: str, loc_lang: str, currency: str, hotels_qty: int,
                    check_in: str, check_out: str, days_stay: int) -> List[Dict[str, Any]]:
    """
    Sorting hotels from lowest to highest price
    :param destination_id: Destination ID
    :type: str
    :param loc_lang: Request language
    :type: str
    :param currency: Request currency
    :type: str
    :param hotels_qty: Hotels qty
    :type: int
    :param check_in: Check in hotel
    :type: str
    :param check_out: Check out hotel
    :type: str
    :param days_stay: Days of stay
    :type: int
    :return: List of Hotel Data Dictionaries
    :type: List[Dict[str, Any]
    """

    lowprice_hotels_list = price_hotels_request(destination_id, loc_lang, currency,
                                                check_in, check_out, days_stay, sort_order='PRICE')

    if len(lowprice_hotels_list) < hotels_qty:
        return lowprice_hotels_list
    else:
        return lowprice_hotels_list[:hotels_qty]
