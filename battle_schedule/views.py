#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import BattleEvent


@login_required
def battle_schedule(request, template='battle-schedule.html'):
    today = (datetime.datetime.today().weekday() + 2) % 7
    tomorrow = (today + 1) % 7
    if tomorrow == 0:
        tomorrow = 1
    day_after = (today + 2) % 7
    if day_after == 0:
        day_after = 1
    today = 7 if today == 0 else today

    print(f" today: {today} - tomorrow: {tomorrow} - day_after: {day_after}")
    battle_events_today = BattleEvent.objects.filter(
        territory__takeover_day=today).order_by('territory__takeover_time')
    battle_events_tomorrow = BattleEvent.objects.filter(
        territory__takeover_day=tomorrow).order_by('territory__takeover_time')
    battle_events_day_after = BattleEvent.objects.filter(
        territory__takeover_day=day_after).order_by('territory__takeover_time')

    battle_events_sunday = BattleEvent.objects.filter(
        territory__takeover_day=1).order_by('territory__takeover_time')
    battle_events_monday = BattleEvent.objects.filter(
        territory__takeover_day=2).order_by('territory__takeover_time')
    battle_events_tuesday = BattleEvent.objects.filter(
        territory__takeover_day=3).order_by('territory__takeover_time')
    battle_events_wednesday = BattleEvent.objects.filter(
        territory__takeover_day=4).order_by('territory__takeover_time')
    battle_events_thursday = BattleEvent.objects.filter(
        territory__takeover_day=5).order_by('territory__takeover_time')
    battle_events_friday = BattleEvent.objects.filter(
        territory__takeover_day=6).order_by('territory__takeover_time')
    battle_events_saturday = BattleEvent.objects.filter(
        territory__takeover_day=7).order_by('territory__takeover_time')
    ctx = {
        'battle_events_today': battle_events_today,
        'battle_events_tomorrow': battle_events_tomorrow,
        'battle_events_day_after': battle_events_day_after,
        'battle_events_sunday': battle_events_sunday,
        'battle_events_monday': battle_events_monday,
        'battle_events_tuesday': battle_events_tuesday,
        'battle_events_wednesday': battle_events_wednesday,
        'battle_events_thursday': battle_events_thursday,
        'battle_events_friday': battle_events_friday,
        'battle_events_saturday': battle_events_saturday,
    }
    return render(request, template, context=ctx)
