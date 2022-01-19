import emoji
import pymongo
from loguru import logger
from telebot import custom_filters

from src.bot import bot
from src.constants import keyboards, keys, states
from utils.filters import IsAdmin

class Bot:
    def __init__(self, telebot):
        self.bot = telebot
        client = pymongo.MongoClient("local host", 27017)
        self.db = client.Msg_Bot

        #register handler
        self.handler()

        #run bot
        logger.info("Bot is working...")
        self.bot.infinity_polling()

        #apply custom filter
        bot.add_custom_filter(IsAdmin())
        bot.add_custom_filter(custom_filters.TextStartsFilter())
	
    def handler(self):

        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.bot.send_message(message.chat.id,
            f"Hiya <strong>{message.chat.first_name}</strong>, how can I help ya?")
            user_info=message.json
            user_info['state']=states.menu
            self.db.users.update_one(
                {'chat.id':message.chat.id},
                {'$set':message.json}, upsert=True)

        @self.bot.message_handler(regexp=emoji.emojize(keys.help))
        def help(message):
            self.send_message(
                message.chat.id,
                '<strong> PyBot:smiling_face_with_sunglasses:</strong> is to randomly connect ya to another person! \n Press `connect` to start!'
                    ,reply_markup=keyboards.main_keyboard)

        @self.bot.message_handler(regexp=emoji.emojize(keys.random_connect))
        def random_connect(message):
            self.send_message(
                message.chat.id,'<strong> Connecting to :man_raising_hand: or :woman_raising_hand:</strong>'
                    ,reply_markup=keyboards.exit)

        @self.bot.message_handler(is_admin=True)
        def admin_of_gp(message):
            self.send_message(
                message.chat.id, 
                '<strong> You are Admin!</strong>')

        @self.bot.message_handler(text=['hi','hello'])
        def text_filter(message):
            self.send_message(message.chat.id, f'Hi {message.from_user.first_name}')

        @self.bot.message_handler(func= lambda message:True)
        def echo(message):
            print(emoji.demojize(message.text))
            self.send_message(message.chat.id,message.text,
            reply_markup=keyboards.main_keyboard)

    def send_message(self, chat_id, text, reply_markup=None, emojize=True):
        if emojize: 
            text = emoji.emojize(text, use_aliases=True)
        self.bot.send_message(chat_id, text, reply_markup=reply_markup)



if __name__ =="__main__":
	logger.info('Bot started')
	bot= Bot(telebot=bot)
