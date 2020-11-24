#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import BattleEvent


@login_required
def battle_schedule(request, template='battle-schedule.html'):
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)

    tomorrow_min = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=1), datetime.time.min)
    tomorrow_max = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=1), datetime.time.max)

    day_after_min = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=2), datetime.time.min)
    day_after_max = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=2), datetime.time.max)

    battle_events_today = BattleEvent.objects.filter(time__range=(today_min, today_max)).order_by('time')
    battle_events_tomorrow = BattleEvent.objects.filter(time__range=(tomorrow_min, tomorrow_max)).order_by('time')
    battle_events_day_after = BattleEvent.objects.filter(time__range=(day_after_min, day_after_max)).order_by('time')
    ctx = {
        'battle_events_today': battle_events_today,
        'battle_events_tomorrow': battle_events_tomorrow,
        'battle_events_day_after': battle_events_day_after,
    }
    return render(request, template, context=ctx)
