"""
Telegram BOT:
    ID: t.me/BattleSchedule_bot
"""

__author__ = 'AlFa7961'

import os
import telebot
import datetime

from ..models import BattleEvent

TOKEN = os.environ['BATTLE_SCHEDULE_TOKEN']

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['ping'])
def ping(m):
    bot.send_message(m.chat.id, "Pong")

@bot.message_handler(commands=['today'])
def today(m):
    msg = bot.send_message(m.chat.id, "Today battles - tell me the type [d/c/lvl1] (*d): ")
    bot.register_next_step_handler(msg, _today_battle_schedules)

def _today_battle_schedules(m):
    today = (datetime.datetime.today().weekday() + 2) % 7
    tomorrow = (today + 1) % 7
    if tomorrow == 0:
        tomorrow = 1
    day_after = (today + 2) % 7
    if day_after == 0:
        day_after = 1
    today = 7 if today == 0 else today

    if not m.text or 'd' in m.text.lower():
        battle_events_today = BattleEvent.objects.filter(
            territory__takeover_day=today, type="defence").order_by('territory__takeover_time')
        _msg = "Today Defence schedules are:"
        for battle_event in battle_events_today:
            _msg += f"\n{battle_event.territory.takeover_time} - {battle_event.territory} {battle_event.alliance}"
        bot.send_message(m.chat.id, _msg)
    elif 'c' in m.text.lower():
        bot.send_message(m.chat.id, "Capture!")
    elif 'lvl1' in m.text.lower():
        bot.send_message(m.chat.id, "Level1 - all can capture!")
    else:
        bot.send_message(m.chat.id, "No valid option, retry!")

@bot.message_handler(commands=['help', 'start'])
def help(m):
    wlcm_msg = "!\nWelcome to @BattleSchedule_bot.\nCommands available:\n/ping - Pong\n/help - Print help message\n/today - Print the schedules for today"

    if m.chat.first_name is not None:
        if m.chat.last_name is not None:
            bot.send_message(m.chat.id, "Hello, " + m.chat.first_name + " " + m.chat.last_name + wlcm_msg)
        else:
            bot.send_message(m.chat.id, "Hello, " + m.chat.first_name + wlcm_msg)
    else:
        bot.send_message(m.chat.id, "Hello, " + m.chat.title + wlcm_msg)

bot.polling(none_stop=True)