import settings
from elephaBot.service.utils.database import *
from elephaBot.service.utils.keyboards import Keyboard
from elephaBot.service.utils.utils import check_user_message
from elephaBot.service.utils.texts import TEXTS
from telebot import TeleBot, types
from telebot.types import Message

bot = TeleBot(settings.BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start_command(message: Message):
    chat_id = str(message.chat.id)

    # Проверка на то, существует ли пользователь в базе
    if not check_user_exists(chat_id):
        add_user(chat_id, str(message.from_user.username))

    user = get_user_by_id(chat_id)

    # Проверка на то, подписался ли пользователь на канал
    user_in_channel = bot.get_chat_member(settings.CHANNEL_ID, int(chat_id))

    if user.completed:
        pass
    elif user_in_channel.status != 'left':
        bot.send_message(
            chat_id,
            TEXTS['/start'][0],
            parse_mode='html',
        )

        bot.send_message(
            chat_id,
            TEXTS['/start'][1],
            reply_markup=Keyboard(['Да']),
            parse_mode='html',
        )
    else:
        bot.send_message(
            chat_id,
            TEXTS['not_subscribed'][0],
            parse_mode='html',
        )


@bot.message_handler(content_types=['contact'])
def contact_handler(message: Message):
    chat_id = str(message.chat.id)
    user = get_user_by_id(chat_id)
    user_condition = BotUserCondition.objects.filter(user=user)[0]

    if user is not None and user_condition is not None and user_condition.on_phone_number_input:
        if user_condition.on_phone_number_input:
            user.phone_number = message.contact.phone_number
            user_condition.on_phone_number_input = False
            user.completed = True

        user_condition.save()
        user.save()

        bot.send_document(
            chat_id,
            File.objects.filter(title='Гайд 1')[0].file.open('rb'),
            caption=TEXTS['last_messages'][0],
            parse_mode='html',
        )
        bot.send_message(
            chat_id,
            TEXTS['last_messages'][1],
            parse_mode='html',
        )


@bot.message_handler(content_types=['text'])
def handle_user_input(message: Message):
    chat_id = str(message.chat.id)
    user = get_user_by_id(chat_id)
    user_condition = BotUserCondition.objects.filter(user=user)[0]

    if user is not None and user_condition is not None:
        if message.text == 'Да':
            # Проверка на то, подписался ли пользователь на канал
            user_in_channel = bot.get_chat_member(settings.CHANNEL_ID, int(chat_id))

            if user_in_channel.status != 'left':
                bot.send_message(
                    chat_id,
                    TEXTS['Конечно'][0],
                    parse_mode='html',
                )

                user_condition.on_first_name_input = True
        else:
            if check_user_message(message.text) or check_user_message(message.text, email=True):
                if user_condition.on_first_name_input:
                    bot.send_message(
                        chat_id,
                        TEXTS['Конечно'][1],
                        parse_mode='html',
                    )

                    user.first_name = message.text
                    user_condition.on_first_name_input = False
                    user_condition.on_second_name_input = True
                elif user_condition.on_second_name_input:
                    # bot.send_message(
                    #     chat_id,
                    #     TEXTS['Конечно'][2],
                    #     parse_mode='html',
                    # )
                    if check_user_message(message.text, email=True):
                        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                        button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
                        keyboard.add(button_phone)

                        bot.send_message(
                            chat_id,
                            TEXTS['Конечно'][3],
                            parse_mode='html',
                            reply_markup=keyboard,
                        )


                        user.second_name = message.text
                        user_condition.on_second_name_input = False
                        user_condition.on_phone_number_input = True
                    else:
                        bot.send_message(
                            chat_id,
                            "Данные введены некорректно, попробуйте снова",
                            parse_mode='html',
                        )

                # elif user_condition.on_email_input:
                #     if check_user_message(message.text, email=True):
                #         keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                #         button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
                #         keyboard.add(button_phone)
                #
                #         bot.send_message(
                #             chat_id,
                #             TEXTS['Конечно'][3],
                #             parse_mode='html',
                #             reply_markup=keyboard,
                #         )
                #
                #         user.email = message.text
                #         user_condition.on_email_input = False
                #         user_condition.on_phone_number_input = True
                #     else:
                #         bot.send_message(
                #             chat_id,
                #             "Данные введены некорректно, попробуйте снова",
                #             parse_mode='html',
                #         )
            else:
                bot.send_message(
                    chat_id,
                    "Данные введены некорректно, попробуйте снова",
                    parse_mode='html',
                )

        user_condition.save()
        user.save()
