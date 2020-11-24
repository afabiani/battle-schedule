#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from django.db import models

logger = logging.getLogger(__name__)


class BattleEvent(models.Model):

    EVENT_CAPTURE = 'capture'
    EVENT_DEFENCE = 'defence'
    EVENT_TYPES = (
        (EVENT_CAPTURE, "Capture"),
        (EVENT_DEFENCE, "Defence")
    )

    time = models.DateTimeField(db_index=True, null=False)
    territory = models.CharField(max_length=1024, blank=False, null=False)
    alliance = models.CharField(max_length=1024, blank=False, null=False)
    type = models.CharField(max_length=255, choices=EVENT_TYPES, null=False, blank=False)
