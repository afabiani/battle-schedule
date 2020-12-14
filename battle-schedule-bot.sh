#!/bin/bash
. /home/ubuntu/.virtualenvs/battle-schedule/bin/activate
. /home/ubuntu/battle-schedule/.override_env

python /home/ubuntu/battle-schedule/manage.py botpolling --username=BattleSchedule_bot
