from django.conf import settings
from django.test import Client, TestCase

# Create your tests here.
client = Client()
secret = settings.ROOT_SECRET
content_type = "application/json"
