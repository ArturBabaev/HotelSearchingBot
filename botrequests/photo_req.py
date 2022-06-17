import requests
import json
from typing import List, Dict, Any
from decouple import config
from loguru import logger
import traceback

KEY = config('KEY')

url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

headers = {
    'x-rapidapi-host': "hotels4.p.rapidapi.com",
    'x-rapidapi-key': KEY
}


def photo_request(hotel_id: str) -> List[Dict[str, Any]]:
    """
    Photo search function by hotel id
    :param hotel_id: hotel id
    :type: str
    :return: List of url photo dictionaries
    :type: List[Dict[str, Any]
    """

    querystring = {"id": hotel_id}

    try:
        response = requests.request("GET", url, headers=headers, params=querystring)

        found_photos = json.loads(response.text)

        photo_list = [{'hotelImages': photo['baseUrl']} for photo in found_photos['hotelImages']]

        return photo_list

    except Exception as error:
        logger.error('error: {} \n{}', error, traceback.format_exc())

        photo_list = []

        return photo_list
