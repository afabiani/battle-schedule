#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import BattleEvent


@admin.register(BattleEvent)
class BattleEventAdmin(admin.ModelAdmin):

    list_display = ('time', 'type', 'system', 'alliance')
    list_select_related = True
    list_filter = ('time', 'type', 'system', 'alliance')
