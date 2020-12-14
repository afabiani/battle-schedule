#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from django.db import models
from django.utils import timezone

logger = logging.getLogger(__name__)


class BattleScheduleNotification(models.Model):

    chat_id = models.CharField(max_length=1024, blank=False, null=False)
    last_update = models.DateTimeField(default=timezone.now, blank=True)
    initialized = models.BooleanField(default=False)
