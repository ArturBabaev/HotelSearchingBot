from telebot import types, TeleBot
from repository.history_repository import HistoryRepositoryDB
from loguru import logger
import traceback


class HistoryController:
    """
    History request processing class
    """

    def __init__(self, bot: TeleBot, history_repository: HistoryRepositoryDB) -> None:
        self.bot = bot
        self.history_repository = history_repository

    def process_history(self, message: types.Message) -> None:
        """
        The method displays a history
        """
        try:
            history = self.history_repository.get_history(message.chat.id)

            if history:
                for hist in history:
                    text_com = 'Команда {} была выбрана {}, ниже приведена история поиска:'.format(hist.command,
                                                                                               hist.data_time)

                    self.bot.send_message(message.chat.id, text=text_com)

                    if hist.hotels_list:
                        text = ''

                        hotels_list_print = []

                        for hotel_data in hist.hotels_list:
                            hotels_list_print.append({'Название отеля': hotel_data['name'],
                                                      'Адрес': hotel_data['address'],
                                                      'Ссылка': 'https://ru.hotels.com/ho{}'.format(hotel_data['hotel_id']),
                                                      'Цена за сутки (руб.)': hotel_data['price'][0],
                                                      'Цена за весь период (руб.)': hotel_data['price'][1],
                                                      'Расстояние от центра': hotel_data['distance_center']})

                        for hotel_data in hotels_list_print:
                            for key, val in hotel_data.items():
                                text += '\n{}: {}'.format(key, val)
                            self.bot.send_message(message.chat.id, text=text, disable_web_page_preview=True)
                            text = ''
                    else:
                        self.bot.send_message(message.chat.id, 'По данному запросу не было найдено гостиниц '
                                                               'на сайте Hotels.com.')
            else:
                self.bot.send_message(message.chat.id, 'На данный момент история поиска отсутствует.')

            self.choose_menu(message)

        except TypeError as error:
            logger.info('user id: {}, command: {}', message.chat.id, '/history')
            logger.error('error: {} \n{}', error, traceback.format_exc())

            self.bot.send_message(message.chat.id, 'Для начала работы с ботом необходимо ввести '
                                                   'либо нажать команду /start')

    def choose_menu(self, message: types.Message) -> None:
        """
        The method for menu selection
        """

        text = 'Выберите дальнейшие действия.'

        keyboard = types.InlineKeyboardMarkup(row_width=1)

        key_menu = types.InlineKeyboardButton(text='Вернуться в меню', callback_data='menu')
        key_end = types.InlineKeyboardButton(text='Завершить работу', callback_data='end')

        keyboard.add(key_menu, key_end)

        self.bot.send_message(message.chat.id, text=text, reply_markup=keyboard)
