"""
WSGI config for botanical_system project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application
project_home = '/home/domain-name/botanical_system'

if project_home not in sys.path:
    sys.path.insert(0, project_home)
    
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'botanical_system.settings')

application = get_wsgi_application()
