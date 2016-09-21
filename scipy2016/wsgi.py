"""
WSGI config for scipy2016 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scipy2016.settings")
sys.path.insert(0, '/Site/scipy_in_2016/scipy')
sys.path.insert(1, '/Site/scipy_in_2016/scipy/scipy2016')
sys.path.insert(2, '/Site/scipy_in_2016/scipy_env/lib/python2.7/site-packages')
activate_this = '/Site/scipy_in_2016/scipy_env/bin/activate_this.py'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
