from telebot import types, TeleBot
from repository.user_repository import UserRepositoryDB
from loguru import logger
import traceback


class HelpController:
    """
    Help request processing class
    """

    def __init__(self, bot: TeleBot, user_repository: UserRepositoryDB) -> None:
        self.bot = bot
        self.user_repository = user_repository

    def process_help(self, message: types.Message) -> None:
        """
        The method displays a list of commands
        """

        text = 'Список доступных команд:' \
               '\n/lowprice — вывод самых дешёвых отелей в городе;' \
               '\n/highprice — вывод самых дорогих отелей в городе;' \
               '\n/bestdeal — вывод отелей, наиболее подходящих по цене и расположению от центра;' \
               '\n/history — вывод истории поиска отелей.'

        try:
            user = self.user_repository.get_user(message.chat.id)
            user.command = '/help'
            self.user_repository.set_user(user)

            self.bot.send_message(message.chat.id, text=text)

        except TypeError as error:
            logger.info('user id: {}, command: {}', message.chat.id, '/help')
            logger.error('error: {} \n{}', error, traceback.format_exc())

            self.bot.send_message(message.chat.id, 'Для начала работы с ботом необходимо ввести '
                                                   'либо нажать команду /start')
