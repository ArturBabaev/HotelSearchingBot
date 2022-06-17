from typing import List, Dict, Any


class History:
    """
    Class describing the history
    """

    def __init__(self, user_id: int, command: str, hotels_list: List[Dict[str, Any]]) -> None:
        self.user_id = user_id
        self.command = command
        self.hotels_list = hotels_list
        self.data_time = None
