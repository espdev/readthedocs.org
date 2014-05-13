#!/usr/bin/env python

import settings.local_srv
from django.core.management import execute_manager
execute_manager(settings.local_srv)
