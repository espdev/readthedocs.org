#!/usr/bin/env python

import settings.postgres_local
from django.core.management import execute_manager
execute_manager(settings.postgres_local)
