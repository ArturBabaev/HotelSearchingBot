from botrequests.photo_req import photo_request
from typing import List
from telebot import types


def check_photo(hotel_id: str, photo_qty: int) -> List[types.InputMediaPhoto]:
    """
    Check for the required number of photos
    :param hotel_id: Hotel ID
    :type: str
    :param photo_qty: Photo qty
    :type: int
    :return: List with url photo
    :type: List[types.InputMediaPhoto]
    """

    photo_list = [types.InputMediaPhoto(val.replace('{size}', 'b'))
                  for new_dict in photo_request(hotel_id)
                  for val in new_dict.values()]

    if len(photo_list) < photo_qty:
        return photo_list
    else:
        return photo_list[:photo_qty]
