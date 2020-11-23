#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

SECRET_KEY = os.getenv('SECRET_KEY', 'r^li-ok%c&hf=^-5%c!pom5see)@v6acex^1s(k0c4z70ep6(l')

# Backend
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DATABASE_NAME', None),
        'USER': os.getenv('DATABASE_USER', None),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', None),
        'HOST': os.getenv('DATABASE_HOST', 'localhost'),
        'PORT': os.getenv('DATABASE_PORT', '5432'),
        'CONN_MAX_AGE': int(os.getenv('DATABASE_CONN_MAX_AGE', 0)),
        'CONN_TOUT': int(os.getenv('DATABASE_CONN_TOUT', 5)),
        'OPTIONS': {
            'connect_timeout': int(os.getenv('DATABASE_CONN_TOUT', 5)),
        }
    }
}
