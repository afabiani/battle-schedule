"""
Telegram BOT:
    ID: t.me/BattleSchedule_bot
"""

__author__ = 'AlFa7961'

import os
import logging
# import telebot
import datetime
from uuid import uuid4
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, Update
from telegram.ext import CommandHandler, InlineQueryHandler, MessageHandler, Filters, CallbackContext
from telegram.utils.helpers import escape_markdown
from django_telegrambot.apps import DjangoTelegramBot

from .models import BattleEvent

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi! Send /help to see the list of available commands.')


def help(bot, update):
    wlcm_msg = "!\nWelcome to @BattleSchedule_bot.\nCommands available:\n/help - Print help message\n/today [d/c/lvl1]- Print the schedules for today, e.g.: /today d"

    if update.message.from_user.first_name is not None:
        if update.message.from_user.last_name is not None:
            bot.sendMessage(update.message.chat_id, "Hello, " + update.message.from_user.first_name + " " + update.message.from_user.last_name + wlcm_msg)
        else:
            bot.sendMessage(update.message.chat_id, "Hello, " + update.message.from_user.first_name + wlcm_msg)
    else:
        bot.sendMessage(update.message.chat_id, "Hello, " + update.message.from_user.username + wlcm_msg)


def today(bot, update):
    text = update.message.text[len('/today')+1:]

    today = (datetime.datetime.today().weekday() + 2) % 7
    tomorrow = (today + 1) % 7
    if tomorrow == 0:
        tomorrow = 1
    day_after = (today + 2) % 7
    if day_after == 0:
        day_after = 1
    today = 7 if today == 0 else today

    if not text or 'd' == text.lower():
        battle_events_today = BattleEvent.objects.filter(
            territory__takeover_day=today, type=BattleEvent.EVENT_DEFENCE).order_by('territory__takeover_time')
        if battle_events_today.count():
            _msg = "Today Defence schedules are:"
            for battle_event in battle_events_today:
                _msg += f"\n{battle_event.territory.takeover_time} - {battle_event.territory} {battle_event.alliance}"
        else:
            _msg = "No Defence scheduled today!"
        bot.sendMessage(update.message.chat_id, _msg)
    elif 'c' == text.lower():
        battle_events_today = BattleEvent.objects.filter(
            territory__takeover_day=today, type=BattleEvent.EVENT_CAPTURE).order_by('territory__takeover_time')
        if battle_events_today.count():
            _msg = "Today Capture schedules are:"
            for battle_event in battle_events_today:
                _msg += f"\n{battle_event.territory.takeover_time} - {battle_event.territory} {battle_event.alliance}"
        else:
            _msg = "No Capture scheduled today!"
        bot.sendMessage(update.message.chat_id, _msg)
    elif 'lvl1' == text.lower():
        battle_events_today = BattleEvent.objects.filter(
            territory__takeover_day=today, type=BattleEvent.EVENT_LEVEL_1).order_by('territory__takeover_time')
        if battle_events_today.count():
            _msg = "Today Level1 schedules are:"
            for battle_event in battle_events_today:
                _msg += f"\n{battle_event.territory.takeover_time} - {battle_event.territory} {battle_event.alliance}"
        else:
            _msg = "No Level1 scheduled today!"
        bot.sendMessage(update.message.chat_id, _msg)
    else:
        bot.sendMessage(update.message.chat_id, "No valid option, retry!")


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    logger.info("Loading handlers for telegram bot")

    # Default dispatcher (this is related to the first bot in settings.DJANGO_TELEGRAMBOT['BOTS'])
    dp = DjangoTelegramBot.dispatcher
    # To get Dispatcher related to a specific bot
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_token')     #get by bot token
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_username')  #get by bot username

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, today))
    # dp.add_handler(MessageHandler(Filters.text & ~Filters.command, today))

    # log all errors
    dp.add_error_handler(error)
