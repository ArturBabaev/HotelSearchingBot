from telebot import types, TeleBot
from repository.user_repository import UserRepositoryDB
from repository.history_repository import HistoryRepositoryDB
from botrequests.city_req import city_request
from service.lowprice import lowprice_hotels
from service.highprice import highprice_hotels
from service.checkphoto import check_photo
from model.history import History
from service.ending import ending
from loguru import logger
from telegram_bot_calendar import DetailedTelegramCalendar
import traceback
from datetime import date, timedelta
import datetime


class PriceController:
    """
    Price request processing class
    """

    def __init__(self, bot: TeleBot, user_repository: UserRepositoryDB, history_repository: HistoryRepositoryDB) -> None:
        self.bot = bot
        self.user_repository = user_repository
        self.history_repository = history_repository

    def process_lowprice(self, message: types.Message) -> None:
        """
        The method calls a method choose_language and passes a message and text
        """

        text = 'Вы выбрали команду /lowprice.\nВыберите язык для ввода названия города.'

        try:
            user = self.user_repository.get_user(message.chat.id)
            user.command = '/lowprice'
            self.user_repository.set_user(user)

            self.choose_language(message, text)

        except TypeError as error:
            logger.info('user id: {}, command: {}', message.chat.id, '/lowprice')
            logger.error('error: {} \n{}', error, traceback.format_exc())


            self.bot.send_message(message.chat.id, 'Для начала работы с ботом необходимо ввести '
                                                   'либо нажать команду /start')

    def process_highprice(self, message: types.Message) -> None:
        """
        The method calls a method choose_language and passes a message and text
        """

        text = 'Вы выбрали команду /highprice.\nВыберите язык для ввода названия города.'

        try:
            user = self.user_repository.get_user(message.chat.id)
            user.command = '/highprice'
            self.user_repository.set_user(user)

            self.choose_language(message, text)

        except TypeError as error:
            logger.info('user id: {}, command: {}', message.chat.id, '/highprice')
            logger.error('error: {} \n{}', error, traceback.format_exc())

            self.bot.send_message(message.chat.id, 'Для начала работы с ботом необходимо ввести '
                                                   'либо нажать команду /start')

    def choose_language(self, message: types.Message, text: str) -> None:
        """
        The method for language selection
        """

        keyboard = types.InlineKeyboardMarkup()

        key_russian = types.InlineKeyboardButton(text='Русский', callback_data='ru_RU')
        key_english = types.InlineKeyboardButton(text='English', callback_data='en_US')

        keyboard.add(key_russian, key_english)

        self.bot.send_message(message.chat.id, text=text, reply_markup=keyboard)

    def language_callback(self, call: types.CallbackQuery) -> None:
        """
        The method for language callback
        """

        user = self.user_repository.get_user(call.message.chat.id)
        user.loc_lang = call.data
        self.user_repository.set_user(user)

        self.choose_city(call.message)

    def choose_city(self, message: types.Message) -> None:
        """
        The method for city selection
        """

        text = ''

        user = self.user_repository.get_user(message.chat.id)

        if user.loc_lang == 'ru_RU':
            text = 'Русский'
        elif user.loc_lang == 'en_US':
            text = 'English'

        text = 'Вы выбрали язык {}. Введите название города.'.format(text)

        self.bot.send_message(message.chat.id, text=text)

        self.bot.register_next_step_handler(message, self.city_callback)

    def city_callback(self, message: types.Message) -> None:
        """
        The method for city callback
        """

        user = self.user_repository.get_user(message.chat.id)
        user.name_city = message.text
        self.user_repository.set_user(user)

        self.choose_location(message)

    def choose_location(self, message: types.Message) -> None:
        """
        The method for location selection
        """

        user = self.user_repository.get_user(message.chat.id)

        text_1 = 'Идет поиск города...'

        msg = self.bot.send_message(message.chat.id, text=text_1)

        text_2 = 'Вы ввели город {}. Уточните местоположение.'.format(user.name_city)

        locations_list = city_request(user.name_city, user.loc_lang)

        try:
            if not locations_list:
                raise ValueError('there is no such city')

            user.city_id_list = [destinationId['destinationId'] for destinationId in locations_list]

            self.user_repository.set_user(user)

            keyboard = types.InlineKeyboardMarkup(row_width=1)

            buttons = [types.InlineKeyboardButton(text=text['caption'],
                                                  callback_data=text['destinationId']) for text in locations_list]

            keyboard.add(*buttons)

            self.bot.edit_message_text(text=text_2, chat_id=message.chat.id, message_id=msg.message_id,
                                       reply_markup=keyboard)

        except ValueError as error:
            logger.info('user id: {}, command: {}', message.chat.id, user.command)
            logger.error('error: {} \n{}', error, traceback.format_exc())

            self.bot.edit_message_text(text='Такого города не существует! Попробуйте еще раз.',
                                       chat_id=message.chat.id, message_id=msg.message_id)

            return self.choose_city(message)

        except TypeError as error:
            logger.info('user id: {}, command: {}', message.chat.id, user.command)
            logger.error('error: {} \n{}', error, traceback.format_exc())

            self.bot.edit_message_text(text='Ошибка доступа к данным сайта! Попробуйте позже.',
                                       chat_id=message.chat.id, message_id=msg.message_id)

    def location_callback(self, call: types.CallbackQuery) -> None:
        """
        The method for location callback
        """

        user = self.user_repository.get_user(call.message.chat.id)
        user.city_id = call.data
        self.user_repository.set_user(user)

        self.choose_check_in_date(call.message)

    def choose_check_in_date(self, message: types.Message) -> None:
        """
        The method for date-in selection
        """

        calendar, step = DetailedTelegramCalendar(calendar_id=1, locale='ru', min_date=date.today()).build()

        self.bot.send_message(message.chat.id, 'Выберите дату заезда!', reply_markup=calendar)

    def choose_check_out_date(self, message: types.Message) -> None:
        """
        The method for date-out selection
        """

        user = self.user_repository.get_user(message.chat.id)

        check_out = datetime.date.fromisoformat(user.check_in) + timedelta(days=1)

        calendar, step = DetailedTelegramCalendar(calendar_id=2, locale='ru', min_date=check_out).build()

        self.bot.send_message(message.chat.id, 'Выберите дату выезда!', reply_markup=calendar)

    def choose_hotel_qty(self, message: types.Message) -> None:
        """
        The method for hotel qty selection
        """

        text = 'Какое количество отелей будем искать? Введите количество отелей, но не больше 25 шт.'

        self.bot.send_message(message.chat.id, text=text)

        self.bot.register_next_step_handler(message, self.choose_hotel)

    def choose_hotel(self, message: types.Message) -> None:
        """
        The method for hotel selection
        """

        msg = self.bot.send_message(message.chat.id, 'Идет поиск отелей...')

        user = self.user_repository.get_user(message.chat.id)

        try:
            user.hotels_qty = int(message.text)

            if 25 < user.hotels_qty or user.hotels_qty <= 0:
                raise ValueError('invalid data')

            city_id = user.city_id
            loc_lang = user.loc_lang
            currency = 'RUB'
            hotels_qty = user.hotels_qty
            check_in = user.check_in
            check_out = user.check_out
            days_stay = (datetime.date.fromisoformat(check_out) - datetime.date.fromisoformat(check_in))

            if user.command == '/lowprice':
                hotels_list = lowprice_hotels(city_id, loc_lang, currency, hotels_qty, check_in, check_out,
                                              days_stay.days)
                user.hotels_list = hotels_list
                self.history_repository.set_history(History(user_id=message.chat.id,
                                                            command='/lowprice',
                                                            hotels_list=hotels_list))
            elif user.command == '/highprice':
                hotels_list = highprice_hotels(city_id, loc_lang, currency, hotels_qty, check_in, check_out,
                                               days_stay.days)
                user.hotels_list = hotels_list
                self.history_repository.set_history(History(user_id=message.chat.id,
                                                            command='/highprice',
                                                            hotels_list=hotels_list))

            self.user_repository.set_user(user)

            if user.hotels_list:
                len_hotels_list = len(user.hotels_list)

                self.bot.edit_message_text(text='По Вашему запросу на сайте Hotels.com я нашел'
                                                       ' {} отел{}.'.format(len_hotels_list, ending(len_hotels_list)),
                                           chat_id=message.chat.id, message_id=msg.message_id)

                self.choose_photo(message)
            else:
                self.bot.edit_message_text(text='На сайте Hotels.com отсутствуют гостиницы в данном городе.',
                                           chat_id=message.chat.id, message_id=msg.message_id)

                self.choose_menu(message)

        except ValueError as error:
            logger.info('user id: {}, command: {}', message.chat.id, user.command)
            logger.error('error: {} \n{}', error, traceback.format_exc())

            self.bot.edit_message_text(text='Пожалуйста введите целое число больше нуля, '
                                                   'но не больше двадцати пяти.',
                                       chat_id=message.chat.id, message_id=msg.message_id)

            return self.choose_hotel_qty(message)

    def choose_photo(self, message: types.Message) -> None:
        """
        The method for photo selection
        """

        text = 'Необходимо ли вывести фото отеля?'

        keyboard = types.InlineKeyboardMarkup()

        key_yes = types.InlineKeyboardButton(text='Да', callback_data='Yes')
        key_no = types.InlineKeyboardButton(text='Нет', callback_data='No')

        keyboard.add(key_yes, key_no)

        self.bot.send_message(message.chat.id, text=text, reply_markup=keyboard)

    def photo_callback(self, message: types.Message) -> None:
        """
        The method for photo callback
        """

        text = 'Какое количество фото необходимо вывести? Введите количество фото, но не больше 10 шт.'

        self.bot.send_message(message.chat.id, text=text)

        self.bot.register_next_step_handler(message, self.hotel_callback_with_photo)

    def hotel_callback_without_photo(self, call: types.CallbackQuery) -> None:
        """
        The method for hotel without photo callback
        """

        self.bot.send_message(call.message.chat.id, 'Ниже приведены данные по отелям:')

        text = ''

        hotels_list_print = []

        for hotel_data in self.user_repository.get_user(call.message.chat.id).hotels_list:
            hotels_list_print.append({'Название отеля': hotel_data['name'],
                                      'Адрес': hotel_data['address'],
                                      'Ссылка': 'https://ru.hotels.com/ho{}'.format(hotel_data['hotel_id']),
                                      'Цена за сутки (руб.)': hotel_data['price'][0],
                                      'Цена за весь период (руб.)': hotel_data['price'][1],
                                      'Расстояние от центра': hotel_data['distance_center']})

        for hotel_data in hotels_list_print:
            for key, val in hotel_data.items():
                text += '\n{}: {}'.format(key, val)
            self.bot.send_message(call.message.chat.id, text=text, disable_web_page_preview=True)
            text = ''

        self.choose_menu(call.message)

    def hotel_callback_with_photo(self, message: types.Message) -> None:
        """
        The method for hotel with photo callback
        """

        user = self.user_repository.get_user(message.chat.id)

        msg = self.bot.send_message(message.chat.id, 'Ниже приведены данные по отелям:')

        try:
            user.photo_qty = int(message.text)

            if 10 < user.photo_qty or user.photo_qty <= 0:
                raise ValueError('invalid data')

            text = ''

            hotels_list_print = []

            photo_qty = user.photo_qty

            for hotel_data in user.hotels_list:
                hotels_list_print.append({hotel_data['hotel_id']:
                                         {'Название отеля': hotel_data['name'],
                                          'Адрес': hotel_data['address'],
                                          'Ссылка': 'https://ru.hotels.com/ho{}'.format(hotel_data['hotel_id']),
                                          'Цена за сутки (руб.)': hotel_data['price'][0],
                                          'Цена за весь период (руб.)': hotel_data['price'][1],
                                          'Расстояние от центра': hotel_data['distance_center']}})

            for hotels in hotels_list_print:
                for hotel_id, hotel_data in hotels.items():
                    for key, val in hotel_data.items():
                        text += '\n{}: {}'.format(key, val)
                    photo_list = check_photo(hotel_id, photo_qty)
                    if len(photo_list) > 0:
                        self.bot.send_media_group(message.chat.id, media=photo_list)
                        self.bot.send_message(message.chat.id, text=text, disable_web_page_preview=True)
                        text = ''
                    else:
                        self.bot.send_message(message.chat.id,
                                              'На сайте Hotels.com отсутвуют фото данной гостиницы.')
                        self.bot.send_message(message.chat.id, text=text, disable_web_page_preview=True)
                        text = ''

            self.user_repository.set_user(user)

            self.choose_menu(message)

        except ValueError as error:
            logger.info('user id: {}, command: {}', message.chat.id, user.command)
            logger.error('error: {} \n{}', error, traceback.format_exc())

            self.bot.edit_message_text(text='Введите целое число больше нуля, но не больше десяти. Пожалуйста!',
                                       chat_id=message.chat.id, message_id=msg.message_id)

            return self.photo_callback(message)

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