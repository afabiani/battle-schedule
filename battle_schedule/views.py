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

    print(f" today: {today} - tomorrow: {tomorrow} - day_after: {day_after}")
    battle_events_today = BattleEvent.objects.filter(
        territory__takeover_day=today).order_by('territory__takeover_time')
    battle_events_tomorrow = BattleEvent.objects.filter(
        territory__takeover_day=tomorrow).order_by('territory__takeover_time')
    battle_events_day_after = BattleEvent.objects.filter(
        territory__takeover_day=day_after).order_by('territory__takeover_time')
    ctx = {
        'battle_events_today': battle_events_today,
        'battle_events_tomorrow': battle_events_tomorrow,
        'battle_events_day_after': battle_events_day_after,
    }
    return render(request, template, context=ctx)
