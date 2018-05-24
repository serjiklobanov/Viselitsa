from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import random
import re
from collections import defaultdict
import config


def start(bot, update):
    chat = update.message.chat_id
    if (chat not in Chats.keys()) or (not Chats[chat]["InGame"]):
        Chats[chat]["InGame"] = True
        Chats[chat]["CurrentWord"] = random.choice(dic)
        Chats[chat]["ShownWord"] = "-" * len(Chats[chat]["CurrentWord"])
        # print(Chats[chat]["ShownWord"])
        bot.send_message(chat_id=chat, text=Chats[chat]["ShownWord"])
    else:
        bot.send_message(chat_id=chat, text=r"Игра уже началась! Используйте /stop, чтобы остановить игру")


def stop(bot, update):
    chat = update.message.chat_id
    if (chat in Chats.keys()) and (Chats[chat]["InGame"]):
        # print(Chats[chat]["ShownWord"])
        Chats[chat]["InGame"] = False
        bot.send_message(chat_id=chat, text="Игра остановлена!")
    else:
        Chats[chat]["InGame"] = False
        bot.send_message(chat_id=chat, text=r"Игра не запущена! Используйте /start, чтобы начать игру")


def get_letter(bot, update):
    massage = update.message.text
    chat = update.message.chat_id
    if len(massage) == 1 and (massage in re.findall("[а-яё]|[А-ЯЁ]", massage)):
        letter = massage.lower()
        # print(letter)
        while Chats[chat]["CurrentWord"].find(letter) != -1:
            x = Chats[chat]["CurrentWord"].find(letter)
            Chats[chat]["ShownWord"] = Chats[chat]["ShownWord"][:x] + letter + Chats[chat]["ShownWord"][x + 1:]
            Chats[chat]["CurrentWord"] = Chats[chat]["CurrentWord"][:x] + "-" + Chats[chat]["CurrentWord"][x + 1:]
        # print(Chats[chat]["ShownWord"])
        # print(Chats[chat]["CurrentWord"])
        bot.send_message(chat_id=chat, text=Chats[chat]["ShownWord"])
    else:
        # print("Введите 1 букву русского алфавита")
        bot.send_message(chat_id=chat, text="Пришлите 1 букву русского алфавита")


def main():
    updater = Updater(config.TOKEN, request_kwargs=config.REQUEST_KWARGS)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.text, get_letter))
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('stop', stop))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    input_file = open(config.WORD_BASE_RUS, 'br').read()
    dic = input_file.decode('utf8').split()
    Chats = defaultdict(lambda: defaultdict())
    main()
