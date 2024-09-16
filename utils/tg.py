from telebot import TeleBot
from config import group_accounts
Token = '7360774553:AAFNtZHCQqh9NrlxiNpC4B0zXx85bzEBAds'
chat_id = '1085423372'

def send_message_success(address, link):
    try:
        str_send = f'✅ {address}\n<a href="{link}" >Tx hash</a > '
        bot = TeleBot(Token)
        bot.send_message(chat_id, str_send, parse_mode='html', disable_notification=True, disable_web_page_preview=True)
    except Exception as error:
        print(error)
def send_message_error(address, errorr):
    try:
        str_send = f'❌ {address}\n{errorr}'
        bot = TeleBot(Token)
        bot.send_message(chat_id, str_send, parse_mode='html', disable_web_page_preview=True)
    except Exception as error:
        print(error)

def send_number(number, address, text, counter, allCount):
    str_send = f'<b>     {group_accounts}</b>\n     Counter: {counter}/{allCount}\n[{number}] <a href="https://scrollscan.com/address/{address}" >{address}</a >\n     {text}'
    bot = TeleBot(Token)
    bot.send_message(chat_id, str_send, parse_mode='html', disable_notification=True, disable_web_page_preview=True)

def send_delay(text):
    str_send = f'<b>     {text}</b>'
    bot = TeleBot(Token)
    bot.send_message(chat_id, str_send, parse_mode='html', disable_notification=True, disable_web_page_preview=True)



