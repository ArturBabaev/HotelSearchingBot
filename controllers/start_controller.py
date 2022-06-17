from telebot import types, TeleBot
from repository.user_repository import UserRepositoryDB
from repository.history_repository import HistoryRepositoryDB
from model.user import User


class StartController:
    """
    Start request processing class
    """

    def __init__(self, bot: TeleBot, user_repository: UserRepositoryDB, history_repository: HistoryRepositoryDB) -> None:
        self.bot = bot
        self.user_repository = user_repository
        self.history_repository = history_repository

    def process_start(self, message: types.Message) -> None:
        """
        The method displays a greeting and command keys
        """

        self.user_repository.set_user(User(user_id=message.chat.id))

        text = 'Привет, я бот "HotelSearchingBot". Я помогу Вам найти самое выгодное предложение ' \
               'на платформе по поиску отелей Hotels.com.\nВыберите необходимую команду. ' \
               '\nДля просмотра описания команд выбирите /help.'

        keyboard = types.InlineKeyboardMarkup()

        key_lowprice = types.InlineKeyboardButton(text='/lowprice', callback_data='lowprice')
        key_highprice = types.InlineKeyboardButton(text='/highprice', callback_data='highprice')
        key_bestdeal = types.InlineKeyboardButton(text='/bestdeal', callback_data='bestdeal')
        key_history = types.InlineKeyboardButton(text='/history', callback_data='history')
        kye_help = types.InlineKeyboardButton(text='/help', callback_data='help')

        keyboard.add(key_lowprice, key_highprice, key_bestdeal, key_history, kye_help)

        self.bot.send_message(message.chat.id, text=text, reply_markup=keyboard)
