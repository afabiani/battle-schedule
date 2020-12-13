#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from django.db import models

logger = logging.getLogger(__name__)


class BattleScheduleNotification(models.Model):

    chat_id = models.CharField(max_length=1024, blank=False, null=False)
    last_update = models.DateTimeField(auto_now=True)
    initialized = models.BooleanField(default=False)
