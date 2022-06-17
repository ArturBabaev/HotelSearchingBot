import sqlite3
from sqlite3 import Connection, Cursor


class DBHelper:
    """
    Database tables creation class
    """

    conn = sqlite3.connect("todo.sqlite.db", check_same_thread=False)
    cur = conn.cursor()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DBHelper, cls).__new__(cls)
            cls.instance.conn.enable_load_extension(True)
            cls.instance.setup()
        return cls.instance

    def get_connector(self) -> Connection:
        """
        Get connector
        :return: connector
        :type: Connection
        """

        return self.conn

    def get_cursor(self) -> Cursor:
        """
        Get cursor
        :return: cursor
        :type: Cursor
        """
        return self.cur

    def setup(self):
        """
        Database tables creation
        """

        user_table_query = "CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY," \
                           " loc_lang VARCHAR(10)," \
                           " name_city VARCHAR(255)," \
                           " command VARCHAR(10)," \
                           " city_id INTEGER," \
                           " city_id_list TEXT," \
                           " hotels_qty INTEGER," \
                           " hotels_list TEXT," \
                           " photo_qty INTEGER," \
                           " photo_id_list TEXT," \
                           " price_min INTEGER," \
                           " price_max INTEGER," \
                           " distance_min REAL," \
                           " distance_max REAL," \
                           " check_in VARCHAR(10)," \
                           " check_out VARCHAR(10))"

        history_table_query = "CREATE TABLE IF NOT EXISTS history (history_id INTEGER PRIMARY KEY AUTOINCREMENT," \
                              " user_id TEXT, " \
                              " command VARCHAR(10)," \
                              " data_time VARCHAR(25)," \
                              " hotels_list TEXT)"

        self.cur.execute(user_table_query)
        self.cur.execute(history_table_query)
        self.conn.commit()
