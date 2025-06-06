"""
WSGI config for final_pjt_back project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""
import os
from dotenv import load_dotenv

# .env 파일 경로 기준은 manage.py와 동일
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'final_pjt_back.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

