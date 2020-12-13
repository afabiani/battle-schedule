"""
Telegram BOT:
    ID: t.me/BattleSchedule_bot
"""

__author__ = 'AlFa7961'

import os
import pytz
import logging
# import telebot
import datetime
from uuid import uuid4
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, Update
from telegram.ext import CommandHandler, InlineQueryHandler, MessageHandler, Filters, CallbackContext
from telegram.utils.helpers import escape_markdown
from django_telegrambot.apps import DjangoTelegramBot

from .models import BattleEvent
from .telegram.models import BattleScheduleNotification

logger = logging.getLogger(__name__)


def _get_days():
    today = (datetime.datetime.today().weekday() + 2) % 7
    tomorrow = (today + 1) % 7
    if tomorrow == 0:
        tomorrow = 1
    day_after = (today + 2) % 7
    if day_after == 0:
        day_after = 1
    today = 7 if today == 0 else today
    return (today, tomorrow, day_after)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi! Send /help to see the list of available commands.')


def help(bot, update):
    wlcm_msg = "!\nWelcome to @BattleSchedule_bot.\n\
Commands available:\n\
/help - Print help message\n\
/today [d/c/lvl1] - Print the schedules for today, e.g.: /today d\n\
/all_captures - Shows the lvl1 Captures for the whole week\n\
/register - Get notified ~45 mins before next Defence event\n\
/unregister - Stop receiving Defence notifications\n"

    if update.message.from_user.first_name is not None:
        if update.message.from_user.last_name is not None:
            bot.sendMessage(update.message.chat_id, "Hello, " + update.message.from_user.first_name + " " + update.message.from_user.last_name + wlcm_msg)
        else:
            bot.sendMessage(update.message.chat_id, "Hello, " + update.message.from_user.first_name + wlcm_msg)
    else:
        bot.sendMessage(update.message.chat_id, "Hello, " + update.message.from_user.username + wlcm_msg)


def today(bot, update):
    text = update.message.text[len('/today')+1:]
    today, tomorrow, day_after = _get_days()
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


def all_captures(bot, update):
    battle_events_sunday = BattleEvent.objects.filter(
        type=BattleEvent.EVENT_LEVEL_1,
        territory__takeover_day=1).order_by('territory__takeover_time')
    battle_events_monday = BattleEvent.objects.filter(
        type=BattleEvent.EVENT_LEVEL_1,
        territory__takeover_day=2).order_by('territory__takeover_time')
    battle_events_tuesday = BattleEvent.objects.filter(
        type=BattleEvent.EVENT_LEVEL_1,
        territory__takeover_day=3).order_by('territory__takeover_time')
    battle_events_wednesday = BattleEvent.objects.filter(
        type=BattleEvent.EVENT_LEVEL_1,
        territory__takeover_day=4).order_by('territory__takeover_time')
    battle_events_thursday = BattleEvent.objects.filter(
        type=BattleEvent.EVENT_LEVEL_1,
        territory__takeover_day=5).order_by('territory__takeover_time')
    battle_events_friday = BattleEvent.objects.filter(
        type=BattleEvent.EVENT_LEVEL_1,
        territory__takeover_day=6).order_by('territory__takeover_time')
    battle_events_saturday = BattleEvent.objects.filter(
        type=BattleEvent.EVENT_LEVEL_1,
        territory__takeover_day=7).order_by('territory__takeover_time')

    _msg = "Lvl1 schedules are:"

    _msg += "\n -- SUNDAY --\n"
    for battle_event in battle_events_sunday:
        _msg += f"\n{battle_event.territory.takeover_time} - [{battle_event.type}] {battle_event.territory} {battle_event.alliance}"
    bot.sendMessage(update.message.chat_id, _msg)

    _msg = "\n -- MONDAY --\n"
    for battle_event in battle_events_monday:
        _msg += f"\n{battle_event.territory.takeover_time} - [{battle_event.type}] {battle_event.territory} {battle_event.alliance}"
    bot.sendMessage(update.message.chat_id, _msg)

    _msg = "\n -- TUESDAY --\n"
    for battle_event in battle_events_tuesday:
        _msg += f"\n{battle_event.territory.takeover_time} - [{battle_event.type}] {battle_event.territory} {battle_event.alliance}"
    bot.sendMessage(update.message.chat_id, _msg)

    _msg = "\n -- WEDNESDAY --\n"
    for battle_event in battle_events_wednesday:
        _msg += f"\n{battle_event.territory.takeover_time} - [{battle_event.type}] {battle_event.territory} {battle_event.alliance}"
    bot.sendMessage(update.message.chat_id, _msg)

    _msg = "\n -- THURSDAY --\n"
    for battle_event in battle_events_thursday:
        _msg += f"\n{battle_event.territory.takeover_time} - [{battle_event.type}] {battle_event.territory} {battle_event.alliance}"
    bot.sendMessage(update.message.chat_id, _msg)

    _msg = "\n -- FRIDAY --\n"
    for battle_event in battle_events_friday:
        _msg += f"\n{battle_event.territory.takeover_time} - [{battle_event.type}] {battle_event.territory} {battle_event.alliance}"
    bot.sendMessage(update.message.chat_id, _msg)

    _msg = "\n -- SATURDAY --\n"
    for battle_event in battle_events_saturday:
        _msg += f"\n{battle_event.territory.takeover_time} - [{battle_event.type}] {battle_event.territory} {battle_event.alliance}"
    bot.sendMessage(update.message.chat_id, _msg)


def register(bot, update):
    BattleScheduleNotification.objects.get_or_create(chat_id=update.message.chat_id)
    _msg = "You have been registered to receive notifications from @BattleScheduler_bot\n\
To stop receiving notifications run the command /unregister"
    bot.sendMessage(update.message.chat_id, _msg)


def unregister(bot, update):
    BattleScheduleNotification.objects.filter(chat_id=update.message.chat_id).delete()
    _msg = "You won't receive notifications from @BattleScheduler_bot anymore\n\
To start receiving notifications again, run the command /register"
    bot.sendMessage(update.message.chat_id, _msg)


def callback_alarm(bot, job):
    # logger.info(f" ------- notify")
    # bot.send_message(chat_id=job.context, text='Alarm')
    today, tomorrow, day_after = _get_days()
    battle_events_today = BattleEvent.objects.filter(
        type=BattleEvent.EVENT_DEFENCE,
        territory__takeover_day=today,
        territory__takeover_time__hour=datetime.datetime.utcnow().hour + 1).order_by('territory__takeover_time')
    if battle_events_today.count():
        _msg = "Today's next Defence events (in about ~45 mins):"
        for battle_event in battle_events_today:
            _msg += f"\n{battle_event.territory.takeover_time} - [{battle_event.type}] {battle_event.territory} {battle_event.alliance}"
            for _notification in BattleScheduleNotification.objects.all():
                delta_time_check = (battle_event.territory.takeover_time - datetime.timedelta(minutes = 45)).replace(tzinfo=pytz.utc)
                if not _notification.initialized or _notification.last_update < delta_time_check:
                    # job.context.message.reply_text("hi")
                    # bot.sendMessage(_notification.chat_id, f'[{_notification.last_update}] hi')
                    bot.sendMessage(_notification.chat_id, _msg)
                    _notification.initialized = True
                    _notification.save()


def callback_timer(bot, update, job_queue):
    bot.send_message(chat_id=update.message.chat_id,
                     text='Starting!')
    job_queue.run_repeating(callback_alarm, 5, context=update.message.chat_id)


def stop_timer(bot, update, job_queue):
    bot.send_message(chat_id=update.message.chat_id,
                     text='Stopped!')
    job_queue.stop()


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
    dp.add_handler(CommandHandler("today", today))
    dp.add_handler(CommandHandler("all_captures", all_captures))

    # manage automatic notifications
    dp.add_handler(CommandHandler("start_timer", callback_timer, pass_job_queue=True))
    dp.add_handler(CommandHandler("stop_timer", stop_timer, pass_job_queue=True))
    dp.add_handler(CommandHandler("register", register))
    dp.add_handler(CommandHandler("unregister", unregister))

    # log all errors
    dp.add_error_handler(error)
