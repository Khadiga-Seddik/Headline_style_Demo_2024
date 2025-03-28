"""
WSGI config for Experiment_2 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NEWSREC_survey.settings")

sys.path.append('/home/ubuntu/demo24/Demo_2024')
application = get_wsgi_application()
