import telebot
from telebot import types
from decouple import config
from repository.user_repository import UserRepositoryDB
from repository.history_repository import HistoryRepositoryDB
from controllers.price_controller import PriceController
from controllers.help_controller import HelpController
from controllers.start_controller import StartController
from controllers.bestdeal_controller import BestdealController
from controllers.history_controller import HistoryController
from telegram_bot_calendar import DetailedTelegramCalendar
from loguru import logger
import traceback
from datetime import date, timedelta
import datetime


TOKEN = config('TOKEN')
bot = telebot.TeleBot(TOKEN)

user_repository_db = UserRepositoryDB()
history_repository_db = HistoryRepositoryDB()
price_controller = PriceController(bot, user_repository_db, history_repository_db)
help_controller = HelpController(bot, user_repository_db)
start_controller = StartController(bot, user_repository_db, history_repository_db)
bestdeal_controller = BestdealController(bot, user_repository_db, history_repository_db)
history_controller = HistoryController(bot, history_repository_db)
logger.add('logs.log', rotation='100 MB')


@bot.message_handler(commands=['start'])
def start_command(message: types.Message) -> None:
    """
    Processing the start command
    """

    start_controller.process_start(message)


@bot.message_handler(commands=['help'])
def help_command(message: types.Message) -> None:
    """
    Processing the help command
    """

    help_controller.process_help(message)


@bot.message_handler(commands=['lowprice'])
def lowprice_command(message: types.Message) -> None:
    """
    Processing the lowprice command
    """

    price_controller.process_lowprice(message)


@bot.message_handler(commands=['highprice'])
def highprice_command(message: types.Message) -> None:
    """
    Processing the highprice command
    """

    price_controller.process_highprice(message)


@bot.message_handler(commands=['bestdeal'])
def bestdeal_command(message: types.Message) -> None:
    """
    Processing the bestdeal command
    """

    bestdeal_controller.process_bestdeal(message)


@bot.message_handler(commands=['history'])
def bestdeal_command(message: types.Message) -> None:
    """
    Processing the history command
    """

    history_controller.process_history(message)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def callback_worker_date_in(call):
    """
    Handling date button requests
    """

    user = user_repository_db.get_user(call.message.chat.id)

    result, key, step = DetailedTelegramCalendar(calendar_id=1, locale='ru', min_date=date.today()).process(call.data)

    if not result and key:
        bot.edit_message_text('Выберите дату заезда!', call.message.chat.id, call.message.message_id, reply_markup=key)
    elif result:
        bot.edit_message_text('Дата заезда {}'.format(result), call.message.chat.id, call.message.message_id)

        user.check_in = result
        user_repository_db.set_user(user)

        if user.command == '/lowprice' or user.command == '/highprice':
            price_controller.choose_check_out_date(call.message)
        elif user.command == '/bestdeal':
            bestdeal_controller.choose_check_out_date(call.message)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2))
def callback_worker_date_out(call):
    """
    Handling date button requests
    """

    user = user_repository_db.get_user(call.message.chat.id)

    check_out = datetime.date.fromisoformat(user.check_in) + timedelta(days=1)

    result, key, step = DetailedTelegramCalendar(calendar_id=2, locale='ru', min_date=check_out).process(call.data)

    if not result and key:
        bot.edit_message_text('Выберите дату выезда!', call.message.chat.id, call.message.message_id, reply_markup=key)
    elif result:
        bot.edit_message_text('Дата выезда {}'.format(result), call.message.chat.id, call.message.message_id)

        user.check_out = result
        user_repository_db.set_user(user)

        if user.command == '/lowprice' or user.command == '/highprice':
            price_controller.choose_hotel_qty(call.message)
        elif user.command == '/bestdeal':
            bestdeal_controller.choose_price_min(call.message)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    """
    Handling button requests
    """

    try:
        user = user_repository_db.get_user(call.message.chat.id)

        if call.data == 'help':
            help_controller.process_help(call.message)

        elif call.data == 'lowprice':
            price_controller.process_lowprice(call.message)

        elif call.data == 'highprice':
            price_controller.process_highprice(call.message)

        elif call.data == 'bestdeal':
            bestdeal_controller.process_bestdeal(call.message)

        elif call.data == 'history':
            history_controller.process_history(call.message)

        elif call.data == 'ru_RU' or call.data == 'en_US':
            if user.command == '/lowprice' or user.command == '/highprice':
                price_controller.language_callback(call)
            elif user.command == '/bestdeal':
                bestdeal_controller.language_callback(call)

        elif call.data in user.city_id_list:
            if user.command == '/lowprice' or user.command == '/highprice':
                price_controller.location_callback(call)
            elif user.command == '/bestdeal':
                bestdeal_controller.location_callback(call)

        elif call.data == 'Yes':
            if user.command == '/lowprice' or user.command == '/highprice':
                price_controller.photo_callback(call.message)
            elif user.command == '/bestdeal':
                bestdeal_controller.photo_callback(call.message)

        elif call.data == 'No':
            if user.command == '/lowprice' or user.command == '/highprice':
                price_controller.hotel_callback_without_photo(call)
            elif user.command == '/bestdeal':
                bestdeal_controller.hotel_callback_without_photo(call)

        elif call.data == 'menu':
            help_controller.process_help(call.message)

        elif call.data == 'end':
            history_repository_db.delete_history(call.message.chat.id)

            bot.send_message(call.message.chat.id, 'Спасибо, что воспользовались ботом "HotelSearchingBot" '
                                                   'ждем Вас снова!')
            bot.send_message(call.message.chat.id, 'Для того, чтобы продолжить работу нажмите /start.')

    except TypeError as error:
        logger.info('user id: {}, command: /{}', call.message.chat.id, call.data)
        logger.error('error: {} \n{}', error, traceback.format_exc())

        bot.send_message(call.message.chat.id, 'Для начала работы с ботом необходимо ввести '
                                               'либо нажать команду /start')


bot.polling(none_stop=True, interval=0)
