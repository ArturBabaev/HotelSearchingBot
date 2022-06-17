from model.history import History
from repository.db_helper import DBHelper
from typing import List
import json
import datetime


class HistoryRepositoryDB:
    """
    Database history table entry class
    """

    def __init__(self):
        self.conn = DBHelper().get_connector()
        self.cur = DBHelper().get_cursor()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(HistoryRepositoryDB, cls).__new__(cls)
        return cls.instance

    def set_history(self, history: History) -> None:
        """
        History table write
        :param history: History
        :type: History
        """

        insert_user_query = "INSERT OR REPLACE INTO history (user_id," \
                            " command," \
                            " data_time," \
                            " hotels_list) VALUES (?,?,?,?)"

        date = datetime.datetime.today()

        args = (history.user_id, history.command, date.strftime("%Y-%m-%d %H:%M:%S"), json.dumps(history.hotels_list))

        self.cur.execute(insert_user_query, args)
        self.conn.commit()

    def get_history(self, user_id: int) -> List[History]:
        """
        Get data from a history table
        :param user_id: User id
        :type: int
        :return: History list
        :type: List[History]
        """

        select_query = "SELECT user_id," \
                       " command," \
                       " data_time," \
                       " hotels_list" \
                       " FROM history WHERE history.user_id = (?)"

        args = (user_id,)
        fetch = self.cur.execute(select_query, args).fetchall()

        history_list = []

        for row in fetch:
            history = History(row[0], row[1], json.loads(row[3]))
            history.data_time = row[2]
            history_list.append(history)

        return history_list

    def delete_history(self, user_id: int) -> None:
        """
        Removing history from a table
        :param user_id: User id
        :type: int
        """

        delete_query = "DELETE FROM history WHERE history.user_id = (?)"

        args = (user_id,)
        self.cur.execute(delete_query, args)
        self.conn.commit()
