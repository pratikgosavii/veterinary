import os

# Set Stream API credentials
os.environ['STREAM_API_KEY'] = 'c7wwttj85hg7'
os.environ['STREAM_API_SECRET'] = 'cgptvrzsttwj9vcebwy25k7y6aqkd6nxh56gkwxhsj3djs989g7k5wraprep926d'

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vetinary.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
