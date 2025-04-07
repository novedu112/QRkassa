import os
import sys

from django.core.wsgi import get_wsgi_application

# sys.path.append('C:/Apache24/htdocs/kassa')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kassa.settings')

application = get_wsgi_application()
