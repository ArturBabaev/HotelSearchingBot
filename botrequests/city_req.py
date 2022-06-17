import requests
import json
from typing import Dict, List, Any, Union
from decouple import config
from bs4 import BeautifulSoup
from loguru import logger
import traceback

KEY = config('KEY')

url = 'https://hotels4.p.rapidapi.com/locations/search'

headers = {
    'x-rapidapi-host': "hotels4.p.rapidapi.com",
    'x-rapidapi-key': KEY
}


def city_request(city: str, loc_lang: str) -> Union[List[Dict[str, Any]], None]:
    """
    Function for determining the city id
    :param city: The city we are looking for
    :type: str
    :param loc_lang: Request language
    :type: str
    :return: List of city Data Dictionaries
    :type: Union[List[Dict[str, Any]], None]
    """

    querystring = {"query": city, "locale": loc_lang}

    try:
        response = requests.request('GET', url, headers=headers, params=querystring)

        found_locations = json.loads(response.text)

        locations_list = [{'destinationId': location['destinationId'],
                           'caption': data_extraction_html(location['caption']),
                           'name': location['name']} for location in found_locations['suggestions'][0]['entities']]

        return locations_list

    except Exception as error:
        logger.error('error: {} \n{}', error, traceback.format_exc())

        return None


def data_extraction_html(location: str) -> str:
    """
    Function to extract data from HTML files
    :param location: HTML to be converted
    :type: str
    :return: converted string
    :type: str
    """

    soup = BeautifulSoup(location, 'html.parser')

    text = soup.get_text()

    return text
