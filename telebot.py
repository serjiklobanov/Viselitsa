from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import random
import re
from collections import defaultdict
import wikipedia
import config


def start(bot, update):
    chat = update.message.chat_id
    if (chat not in Chats.keys()) or (not Chats[chat]["InGame"]):
        Chats[chat]["InGame"] = True
        Chats[chat]["Lives"] = 9
        Chats[chat]["CurrentWord"] = random.choice(dic).upper()
        print(Chats[chat]["CurrentWord"])
        Chats[chat]["Save"] = Chats[chat]["CurrentWord"]
        Chats[chat]["ShownWord"] = "—" * len(Chats[chat]["CurrentWord"])
        answer = "Слово: " + Chats[chat]["ShownWord"] + "\n" + "Жизни: " + str(Chats[chat]["Lives"])
        print(answer)
        bot.send_message(chat_id=chat, text=answer)
    else:
        bot.send_message(chat_id=chat, text=r"Игра уже началась! Используйте /stop, чтобы остановить игру")


def stop(bot, update):
    chat = update.message.chat_id
    if (chat in Chats.keys()) and (Chats[chat]["InGame"]):
        Chats[chat]["InGame"] = False
        bot.send_message(chat_id=chat, text="Игра остановлена!")
    else:
        Chats[chat]["InGame"] = False
        bot.send_message(chat_id=chat, text=r"Игра не запущена! Используйте /start, чтобы начать игру")


def get_wiki(chat):
    res = Chats[chat]["Save"] + "\n" + wikipedia.summary(Chats[chat]["Save"], chars=200) \
          + "\n" + wikipedia.page(Chats[chat]["Save"]).url
    return res


def get_letter(bot, update):
    massage = update.message.text
    chat = update.message.chat_id
    if Chats[chat]["InGame"]:
        if len(massage) == 1 and (massage in re.findall("[а-яё]|[А-ЯЁ]", massage)):
            letter = massage.upper()
            if Chats[chat]["CurrentWord"].find(letter) == -1:
                Chats[chat]["Lives"] -= 1
                if Chats[chat]["Lives"] == 0:
                    Chats[chat]["InGame"] = False
                    bot.send_message(chat_id=chat, text="К сожалению, вы проиграли(\n" + "Загаданное слово:\n"
                                     + get_wiki(chat))
                    bot.send_message(chat_id=chat, text=r"Используйте /start, чтобы начать игру")
                else:
                    answer = "Неверно!" + "\n" + "Слово: " + Chats[chat]["ShownWord"] \
                             + "\n" + "Жизни: " + str(Chats[chat]["Lives"])
                    bot.send_message(chat_id=chat, text=answer)
            else:
                while Chats[chat]["CurrentWord"].find(letter) != -1:
                    x = Chats[chat]["CurrentWord"].find(letter)
                    Chats[chat]["ShownWord"] = \
                        Chats[chat]["ShownWord"][:x] + letter + Chats[chat]["ShownWord"][x + 1:]
                    Chats[chat]["CurrentWord"] = \
                        Chats[chat]["CurrentWord"][:x] + "—" + Chats[chat]["CurrentWord"][x + 1:]
                if Chats[chat]["ShownWord"].find("—") != -1:
                    answer = "Верно!\nСлово: " + Chats[chat]["ShownWord"] + "\n" + "Жизни: " + str(Chats[chat]["Lives"])
                    bot.send_message(chat_id=chat, text=answer)
                else:
                    Chats[chat]["InGame"] = False
                    bot.send_message(chat_id=chat, text="Вы победили!\n" + "Загаданное слово:\n" +
                                                        get_wiki(chat))
                    bot.send_message(chat_id=chat, text=r"Используйте /start, чтобы начать игру")
        else:
            bot.send_message(chat_id=chat, text="Пришлите 1 букву русского алфавита")
    else:
        Chats[chat]["InGame"] = False
        bot.send_message(chat_id=chat, text=r"Игра не запущена! Используйте /start, чтобы начать игру")


def main():
    wikipedia.set_lang("ru")
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
