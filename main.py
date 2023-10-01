
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

import re, os
from datetime import datetime

import content_messages, config


secret = config.secret
TOKEN = config.TOKEN

bot = telebot.TeleBot(TOKEN, threaded=False)
bot.remove_webhook()
# bot.set_webhook(url=config.set_webhook.format(secret))

developer_id = config.developer_id
admin_id = config.admin_id


# app = Flask(__name__)

# @app.route('/{}'.format(secret), methods=["POST"])
# def telegram_webhook():
#     req = request.stream.read().decode('utf-8')
#     bot.process_new_updates([telebot.types.Update.de_json(req)])
#     return "200"



def main_menu_buttons():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
    markup.row(content_messages.make_order_button)
    markup.row(content_messages.info_button)
    return markup


@bot.message_handler(regexp=content_messages.info_button)
@bot.message_handler(commands=['info'])
def command_info(message):
    bot.reply_to(message, content_messages.info, parse_mode='html')


def confirmation_button():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    markup.row(content_messages.yes_button)
    markup.row(content_messages.cannel_button)
    return markup

def cancel_button():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    markup.row(content_messages.cannel_button)
    return markup

def check_if_canceled(message, order_data = None):
    if message.text == content_messages.cannel_button:
        bot.send_message(message.from_user.id, content_messages.order_canceled, parse_mode='html')
        command_hello(message)

        # try:
        #     if order_data:
        #         os.remove(order_data['item_video'])
        # except Exception as e:
        #     print(e)
        #     bot.send_message(developer_id, str(e))
        return True
    else:
        return False


@bot.message_handler(regexp=content_messages.make_order_button)
def start_order(message):
    bot.send_message(message.from_user.id, content_messages.howto_order, disable_web_page_preview=True, parse_mode='html', reply_markup=cancel_button())
    bot.register_next_step_handler(message, get_post_link)


def get_post_link(message):
    if check_if_canceled(message): return

    if message.text != None and ("https://www.instagram.com/reel" in message.text or "https://www.instagram.com/p/" in message.text):
        item_video_url = message.text.replace("instagram.com","ddinstagram.com").split(' ')[0]
        # response = requests.get(message.text.replace("instagram.com","ddinstagram.com").split(' ')[0])
        # if response.status_code == 200:
        try:
            # bot.reply_to(message, "загрузка 🔄", parse_mode='html')

            # soup = BeautifulSoup(response.content, 'html.parser')

            # video_url = "https://www.ddinstagram.com" + soup.find('meta', {'name': 'twitter:player:stream'})['content']
            # video_description = soup.find('meta', {'name': 'description'})['content']

            # video_response = requests.get(video_url)
            # file_name = str(message.from_user.id) + video_url.replace('https://www.ddinstagram.com', '').replace('/', '') + '.mp4'

            # with open(file_name, 'wb') as video_file:
            #     video_file.write(video_response.content)

            # bot.send_video(message.from_user.id, open(file_name, 'rb'), caption=video_description, parse_mode='html')
            bot.send_message(message.from_user.id, f"<a href='{item_video_url}'>ссылка</a>", disable_web_page_preview=False, parse_mode='html', reply_markup=cancel_button())
            # try: os.remove(file_name)
            # except Exception as e:
            #     print(e)
            #     bot.send_message(developer_id, str(e))


            # order_data = {"item_description": video_description, "item_video": file_name, "item_video_url": message.text}
            order_data = {"item_video_url": item_video_url}
            bot.send_message(message.from_user.id, "<b>Вы точно хотите купить эти часы?</b>", parse_mode='html', reply_markup=confirmation_button())
            bot.register_next_step_handler(message, ask_name, order_data)
            return

        except Exception as e:
            print(e)
            bot.send_message(developer_id, str(e))
            bot.send_message(message.from_user.id, "❌ <b>Ошибочка! Свяжитесь с администратором!</b>", parse_mode='html')
            command_hello(message)
            return


    bot.send_message(message.from_user.id, f"<b>неправильная ссылка ❌</b>\n{content_messages.howto_order}", disable_web_page_preview=True, parse_mode='html', reply_markup=cancel_button())
    bot.register_next_step_handler(message, get_post_link)



def ask_name(message, order_data):
    if check_if_canceled(message, order_data): return

    bot.send_message(message.from_user.id, "<b>👤 Введите свое полное имя и фамилию:</b>", parse_mode='html', reply_markup=cancel_button())
    bot.register_next_step_handler(message, get_name, order_data)

def get_name(message, order_data):
    if check_if_canceled(message, order_data): return

    if message.text == None or len(message.text) < 1:
        bot.send_message(message.from_user.id, "<b>❌ Ошибка\n👤 Введите свое полное имя и фамилию:</b>", parse_mode='html', reply_markup=cancel_button())
        bot.register_next_step_handler(message, get_name, order_data)

    else:
        order_data["name"] = message.text

        bot.send_message(message.from_user.id, "<b>📞 Введите ваш рабочий номер телефона:</b>", parse_mode='html', reply_markup=cancel_button())
        bot.register_next_step_handler(message, get_phone, order_data)

def get_phone(message, order_data):
    if check_if_canceled(message, order_data): return

    if message.text == None or len(message.text) < 9 or not re.search(r'\+\d+|\d+', message.text):
        bot.send_message(message.from_user.id, "<b>❌ Ошибка\n📞 Введите действительный номер телефона:</b>", parse_mode='html', reply_markup=cancel_button())
        bot.register_next_step_handler(message, get_phone, order_data)

    else:
        order_data["phone_number"] = message.text

        try:
            markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
            for region in content_messages.regions:
                markup.add(region)
            markup.add(content_messages.cannel_button)

            bot.send_message(message.from_user.id, "<b>📍 Выберите ваш регион для бесплатной доставки:</b>", parse_mode='html', reply_markup=markup)
            bot.register_next_step_handler(message, get_region, order_data)
        except Exception as e:
            print(e)
            bot.send_message(developer_id, str(e))
            bot.send_message(message.from_user.id, "❌ <b>Ошибочка! Свяжитесь с администратором!</b>", parse_mode='html')
            command_hello(message)
            return

def get_region(message, order_data):
    if check_if_canceled(message, order_data): return

    if message.text == content_messages.regions[0]:  # Ташкент
        keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(KeyboardButton(text="Отправить своё местоположение 📍", request_location=True))
        keyboard.add(content_messages.cannel_button)

        bot.send_message(message.from_user.id, "<b>📍 Отправьте локацию:</b>", parse_mode='html', reply_markup=keyboard)
        bot.register_next_step_handler(message, get_geolocation_tashkent, order_data)

    elif message.text in content_messages.regions:
        order_data["region"] = message.text
        ask_bts_office(message, order_data)

    else:
        try:
            markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
            for region in content_messages.regions:
                markup.add(region)
            markup.add(content_messages.cannel_button)

            bot.send_message(message.from_user.id, "<b>❌ Ошибка, выберите регион из списка\n📍 Выберите ваш регион:</b>", parse_mode='html', reply_markup=markup)
            bot.register_next_step_handler(message, get_region, order_data)
        except Exception as e:
            print(e)
            bot.send_message(developer_id, str(e))
            bot.send_message(message.from_user.id, "❌ <b>Ошибочка! Свяжитесь с администратором!</b>", parse_mode='html')
            command_hello(message)
            return

def ask_bts_office(message, order_data): # works only for orders in regions
    if check_if_canceled(message, order_data): return

    try:
        for office in os.listdir(f'bts-offices/{order_data["region"]}'):
            with open(f'bts-offices/{order_data["region"]}/{office}', 'rb') as photo:
                bot.send_photo(message.from_user.id, photo=photo, caption=office.split('#')[0], parse_mode='html')
                bot.send_location(message.from_user.id, latitude=office.split('#')[1].replace('.jpg', '').split(',')[0], longitude=office.split('#')[1].replace('.jpg', '').split(',')[1])
            
        markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        for office in os.listdir(f'bts-offices/{order_data["region"]}'):
            markup.add(office.split('#')[0])
        markup.add(content_messages.cannel_button)

        bot.send_message(message.from_user.id, "<b>📦 Выберите оффис BTS-Express где вы хотите получить ваш заказ:</b>", parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler(message, get_bts_office, order_data)
    except Exception as e:
            print(e)
            bot.send_message(developer_id, str(e))
            bot.send_message(message.from_user.id, "❌ <b>Ошибочка! Свяжитесь с администратором!</b>", parse_mode='html')
            command_hello(message)
            return

def get_bts_office(message, order_data): # works only for orders in regions
    if check_if_canceled(message, order_data): return

    for office in os.listdir(f'bts-offices/{order_data["region"]}'):
        if message.text == office.split('#')[0]:
            order_data["bts_office"] = office

            bot.send_message(message.from_user.id, "<b>Ваш заказ:</b>", parse_mode='html')

            order = f"""
<b>👤 Имя:</b> {order_data['name']}
<b>📞 Номер:</b> {order_data['phone_number']}
<b>📍 Адресс:</b> {office.split('#')[0]}
<b>⌚️ Товар:</b> <a href='{order_data['item_video_url']}'>часы</a>"""

            # bot.send_video(message.from_user.id, open(order_data['item_video'], 'rb'), caption=order, parse_mode='html')
            bot.send_message(message.from_user.id, order, disable_web_page_preview=False, parse_mode='html')
            try:
                with open(f'bts-offices/{order_data["region"]}/{office}', 'rb') as photo:
                    bot.send_photo(message.from_user.id, photo=photo, caption=office.split('#')[0], parse_mode='html')
                bot.send_location(message.from_user.id, latitude=office.split('#')[1].replace('.jpg', '').split(',')[0], longitude=office.split('#')[1].replace('.jpg', '').split(',')[1])
            except Exception as e:
                print(e)
                bot.send_message(developer_id, str(e))
            bot.send_message(message.from_user.id, "<b>✅ Всё верно?</b>\nПодтвердите ваш заказ нажав на кнопку ниже", parse_mode='html', reply_markup=confirmation_button())
            bot.register_next_step_handler(message, valide_purchase, order_data, False)


def get_geolocation_tashkent(message, order_data): # works only for orders in Tashkent
    if check_if_canceled(message, order_data): return

    if message.location == None:
        keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(KeyboardButton(text="Отправить своё местоположение 📍", request_location=True))
        keyboard.add(content_messages.cannel_button)

        bot.send_message(message.from_user.id, "<b>❌ Ошибка\n📍 Отправьте локацию для получения доставки:</b>", parse_mode='html', reply_markup=keyboard)
        bot.register_next_step_handler(message, get_geolocation_tashkent, order_data)

    else:
        order_data["address"] = {"longitude": message.location.longitude, "latitude": message.location.latitude}
        bot.send_message(message.from_user.id, "<b>Ваш заказ:</b>", parse_mode='html')

        order = f"""
<b>👤 Имя:</b> {order_data['name']}
<b>📞 Номер:</b> {order_data['phone_number']}
<b>📍 Адресс:</b> локация
<b>⌚️ Товар:</b> <a href='{order_data['item_video_url']}'>часы</a>"""

        # bot.send_video(message.from_user.id, open(order_data['item_video'], 'rb'), caption=order, parse_mode='html')
        bot.send_message(message.from_user.id, order, disable_web_page_preview=False, parse_mode='html')
        bot.send_location(message.from_user.id, latitude=order_data['address']['latitude'], longitude=order_data['address']['longitude'])
        bot.send_message(message.from_user.id, "<b>✅ Всё верно?</b>\nПодтвердите ваш заказ нажав на кнопку ниже", parse_mode='html', reply_markup=confirmation_button())
        bot.register_next_step_handler(message, valide_purchase, order_data, True)


def valide_purchase(message, order_data, is_tashkent: bool):
    if check_if_canceled(message, order_data): return

    bot.send_message(message.from_user.id, "<b>Спасибо за ваш заказ! 🙏</b>\nАдминистратор скоро свяжется с вами!", parse_mode='html', reply_markup=main_menu_buttons())

    for admin in admin_id:
        order = f"""
#order{str(message.from_user.id)}_{str(datetime.now().strftime("%d%m%Y_%H%M%S"))}_{str(order_data['item_video_url']).replace('https://www.ddinstagram.com/', '').split('/')[1].replace('_', '')}
<b>👤 Имя:</b> {str(order_data['name'])}
<b>🆔 Телеграм:</b> <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>  @{message.from_user.username}
<b>📞 Номер:</b> {order_data['phone_number']}
<b>📍 Адресс:</b> {order_data['bts_office'].split('#')[0] if 'bts_office' in order_data else f'{order_data["address"]["latitude"]},{order_data["address"]["longitude"]}'}
<b>⌚️ Товар:</b> <a href='{order_data['item_video_url']}'>часы</a>"""

        # bot.send_video(admin, open(order_data['item_video'], 'rb'), caption=order, parse_mode='html')
        if is_tashkent:
            r = bot.send_message(admin, order, disable_web_page_preview=False, parse_mode='html')
            bot.send_location(admin, latitude=order_data['address']['latitude'], longitude=order_data['address']['longitude'], reply_to_message_id=r.message_id)
        
        else:
            r = bot.send_message(admin, order, disable_web_page_preview=False, parse_mode='html')
            with open(f'bts-offices/{order_data["region"]}/{order_data["bts_office"]}', 'rb') as photo:
                bot.send_photo(admin, photo=photo, caption=order_data["bts_office"].split('#')[0], reply_to_message_id=r.message_id, parse_mode='html')

        # try: os.remove(order_data['item_video'])
        # except Exception as e:
        #     print(e)
        #     bot.send_message(developer_id, str(e))


@bot.message_handler(content_types=['text'])
@bot.message_handler(commands=['start', 'help'])
def command_hello(message):
    if message.chat.type == "private":
        try: bot.send_message(message.from_user.id, content_messages.greeting, parse_mode='html', reply_markup=main_menu_buttons())
        except Exception as e:
            print(e)
            bot.send_message(developer_id, str(e))



print("bot has been started")
bot.polling(none_stop=True)

# luxurywatch@1234