import telebot
from telebot import types
import webbrowser

bot = telebot.TeleBot('6154099183:AAEOPknH0R_G_GtRAIkMW-Zbo3Ykb2FVJys')


@bot.message_handler(commands=['start']) #START LAYOUT
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1=types.KeyboardButton('Info')
    btn2=types.KeyboardButton('Website')
    btn3=types.KeyboardButton('Edit photo')
    btn4=types.KeyboardButton('Delete photo')
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


def on_click(message):
    if message.text == 'Info':
        bot.send_message(message.chat.id, 'Website')
    elif message.text == 'Delete photo':
        bot.send_message(message.chat.id, 'deleted')
    elif message.text == 'Website':
        bot.send_message(message.chat.id, 'website')
    elif message.text == 'Edit photo':
        bot.send_message(message.chat.id, 'edited')



@bot.message_handler(commands=['info']) #INFO BUTTON
def main(message):
    bot.send_message(message.chat.id, 'Help information')

@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('https://www.google.com')


@bot.message_handler(content_types=['photo']) #PHOTO HANDLING
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1=types.InlineKeyboardButton('Info', callback_data='info')
    btn2=types.InlineKeyboardButton('Website', url='https://www.google.com')
    btn3=types.InlineKeyboardButton('Edit photo', callback_data='edit')
    btn4=types.InlineKeyboardButton('Delete photo', callback_data='delete')
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    bot.reply_to(message, 'Nice photo!', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True) 
def callback_message(callback):
    if callback.data == 'edit':
        bot.edit_message_text('Edited text', callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'info':
        bot.send_message(callback.message.chat.id, 'Help information')
    elif callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id-1)
    

bot.infinity_polling()
