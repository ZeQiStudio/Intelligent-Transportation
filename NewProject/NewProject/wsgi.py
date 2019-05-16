#-*- coding: utf-8 -*-

"""
WSGI config for NewProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""


import os
import sys
from django.core.wsgi import get_wsgi_application

apache_configuration= os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(project)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NewProject.settings")

application = get_wsgi_application()

sys.path.append('F:\Python36\Lib\site-packages')
