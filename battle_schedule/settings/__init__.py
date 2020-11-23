#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .base import *  # noqa

from .production import *  # noqa

try:
    from .local import *  # noqa
except Exception:
    pass
