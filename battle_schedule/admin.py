#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Territory, BattleEvent


@admin.register(Territory)
class TerritoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'takeover_day', 'takeover_time')
    list_select_related = True
    list_filter = ('name', 'takeover_day', 'takeover_time')


@admin.register(BattleEvent)
class BattleEventAdmin(admin.ModelAdmin):

    list_display = ('territory', 'type', 'alliance', 'notes')
    list_select_related = True
    list_filter = ('territory', 'type', 'alliance')
