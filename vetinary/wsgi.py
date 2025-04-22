import os
import sys

# Assuming your Django settings file is at '/home/vetinarybackend/veterinary/'
path = '/home/vetinarybackend/veterinary/'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['STREAM_API_KEY'] = 'c7wwttj85hg7'
os.environ['STREAM_API_SECRET'] = 'cgptvrzsttwj9vcebwy25k7y6aqkd6nxh56gkwxhsj3djs989g7k5wraprep926d'


# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'vetinary.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
