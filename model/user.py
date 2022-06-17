class User:
    """
    Class describing the user
    """

    def __init__(self, user_id: int, loc_lang: str = 'ru_RU') -> None:
        self.user_id = user_id
        self.loc_lang = loc_lang
        self.name_city = None
        self.command = None
        self.city_id = None
        self.city_id_list = None
        self.hotels_qty = None
        self.hotels_list = None
        self.photo_qty = None
        self.photo_id_list = None
        self.price_min = None
        self.price_max = None
        self.distance_min = None
        self.distance_max = None
        self.check_in = None
        self.check_out = None
