import telebot
from telebot import types
import webbrowser
import sqlite3 #sdlrghaeiguhzisnaljkesfnaljwbv
#import TopGTeleBot.config as config #ksjrng


bot = telebot.TeleBot(config.BOT_TOKEN)
name = None


@bot.message_handler(commands=['start']) #START LAYOUT
def start(message):
    conn = sqlite3.connect('topgtelebot.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()
    
    bot.send_message(message.chat.id, 'Hello! Please, enter your name')
    bot.register_next_step_handler(message, user_name)


def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Enter your password')
    bot.register_next_step_handler(message, user_pass)


def user_pass(message):
    password = message.text.strip()

    conn = sqlite3.connect('topgtelebot.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (name, password))
    conn.commit()
    cur.close()
    conn.close()

    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Info')
    btn2 = types.KeyboardButton('Website')
    btn3 = types.KeyboardButton('Edit photo')
    btn4 = types.KeyboardButton('Delete photo')
    btn5 = types.KeyboardButton('Payment')
    btn6 = types.KeyboardButton('Payment')
    
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    markup.row(btn5)


    bot.send_message(message.chat.id, 'Successful! Welcome!')
    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


def on_click(message):
    if message.text == 'Info':
        bot.send_message(message.chat.id, 'Info')
    elif message.text == 'Delete photo':
        bot.send_message(message.chat.id, 'deleted')
    elif message.text == 'Website':
        webbrowser.open('https://www.google.com')
    elif message.text == 'Edit photo':
        bot.send_message(message.chat.id, 'edited')
    elif message.text == 'Payment':
        bot.send_invoice(message.chat.id, 'Buy Chebureki', 'Kupit chebureki besplatno', 'invoice', config.PAYMENT_TOKEN, 'RUB', [types.LabeledPrice('Chebureki', 5 * 100)])

    bot.register_next_step_handler(message, on_click)


@bot.message_handler(commands=['info']) #INFO BUTTON
def main(message):
    bot.send_message(message.chat.id, 'Help information')

@bot.message_handler(commands=['site', 'website']) #WEBSITE BUTTON
def site(message):
    webbrowser.open('https://www.google.com')


@bot.callback_query_handler(func=lambda callback: True) 
def callback_message(callback):
    if callback.data == 'edit':
        bot.edit_message_text('Edited text', callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'info':
        bot.send_message(callback.message.chat.id, 'Help information')
    elif callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id-1)
    

bot.infinity_polling()
