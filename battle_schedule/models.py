#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from django.db import models
from django.db.models import signals

logger = logging.getLogger(__name__)


class Territory(models.Model):

    TAKEOVER_DAY_1 = 1
    TAKEOVER_DAY_2 = 2
    TAKEOVER_DAY_3 = 3
    TAKEOVER_DAY_4 = 4
    TAKEOVER_DAY_5 = 5
    TAKEOVER_DAY_6 = 6
    TAKEOVER_DAY_7 = 7
    TAKEOVER_DAYS = (
        (TAKEOVER_DAY_1, "Sunday"),
        (TAKEOVER_DAY_2, "Monday"),
        (TAKEOVER_DAY_3, "Tuesday"),
        (TAKEOVER_DAY_4, "Wednesday"),
        (TAKEOVER_DAY_5, "Thursday"),
        (TAKEOVER_DAY_6, "Friday"),
        (TAKEOVER_DAY_7, "Saturday"),
    )

    name = models.CharField(max_length=1024, blank=False, null=False)
    takeover_day = models.IntegerField(choices=TAKEOVER_DAYS, null=False, blank=False)
    takeover_time = models.TimeField(null=False)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ("name",)
        verbose_name_plural = 'Territories'

class BattleEvent(models.Model):

    EVENT_NEUTRAL = 'neutral'
    EVENT_CAPTURE = 'capture'
    EVENT_DEFENCE = 'defence'
    EVENT_LEVEL_1 = 'lvl 1 all can capture'
    EVENT_TYPES = (
        (EVENT_NEUTRAL, "Neutral"),
        (EVENT_CAPTURE, "Capture"),
        (EVENT_DEFENCE, "Defence"),
        (EVENT_LEVEL_1, "Lvl 1 All can capture")
    )

    territory = models.ForeignKey(Territory, on_delete=models.CASCADE)
    alliance = models.CharField(max_length=1024, blank=False, null=False, default="No alliance set.")
    type = models.CharField(max_length=255, choices=EVENT_TYPES, null=False, blank=False, default=EVENT_NEUTRAL)
    notes = models.TextField(blank=True, null=True)


def territory_post_save(instance, *args, **kwargs):
    """
    Used to fill the average rating field on OverallRating change.
    """
    if not BattleEvent.objects.filter(territory=instance).count():
        BattleEvent.objects.create(territory=instance)


signals.post_save.connect(territory_post_save, sender=Territory)
