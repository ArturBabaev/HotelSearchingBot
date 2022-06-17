from model.user import User
from repository.db_helper import DBHelper
import json


class UserRepositoryDB:
    """
    Database user table entry class
    """

    def __init__(self):
        self.conn = DBHelper().get_connector()
        self.cur = DBHelper().get_cursor()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(UserRepositoryDB, cls).__new__(cls)
        return cls.instance

    def set_user(self, user: User) -> None:
        """
        Users table write
        :param user: User
        :type: User
        """

        insert_user_query = "INSERT OR REPLACE INTO users (user_id," \
                            " loc_lang," \
                            " name_city," \
                            " command," \
                            " city_id," \
                            " city_id_list," \
                            " hotels_qty," \
                            " hotels_list," \
                            " photo_qty," \
                            " photo_id_list," \
                            " price_min," \
                            " price_max," \
                            " distance_min," \
                            " distance_max," \
                            " check_in," \
                            " check_out) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        city_id_list = ""
        if user.city_id_list is not None:
            city_id_list = ','.join(user.city_id_list)

        photo_id_list = ""
        if user.photo_id_list is not None:
            photo_id_list = ','.join(user.photo_id_list)

        args = (user.user_id, user.loc_lang, user.name_city, user.command, user.city_id, city_id_list, user.hotels_qty,
                json.dumps(user.hotels_list), user.photo_qty, photo_id_list, user.price_min, user.price_max,
                user.distance_min, user.distance_max, user.check_in, user.check_out)
        self.cur.execute(insert_user_query, args)
        self.conn.commit()

    def get_user(self, user_id: int) -> User:
        """
        Get data from a users table
        :param user_id: User id
        :type: int
        :return: Users list
        :type: User
        """

        select_query = "SELECT user_id," \
                       " loc_lang," \
                       " name_city," \
                       " command," \
                       " city_id," \
                       " city_id_list," \
                       " hotels_qty," \
                       " hotels_list," \
                       " photo_qty," \
                       " photo_id_list," \
                       " price_min," \
                       " price_max," \
                       " distance_min," \
                       " distance_max," \
                       " check_in," \
                       " check_out" \
                       " FROM users WHERE users.user_id = (?)"

        args = (user_id,)
        fetch = self.cur.execute(select_query, args).fetchone()

        user = User(fetch[0], fetch[1])
        user.name_city = fetch[2]
        user.command = fetch[3]
        user.city_id = fetch[4]
        user.city_id_list = str(fetch[5]).split(",")
        user.hotels_qty = fetch[6]
        user.hotels_list = json.loads(fetch[7])
        user.photo_qty = fetch[8]
        user.photo_id_list = str(fetch[9]).split(",")
        user.price_min = fetch[10]
        user.price_max = fetch[11]
        user.distance_min = fetch[12]
        user.distance_max = fetch[13]
        user.check_in = fetch[14]
        user.check_out = fetch[15]

        return user
