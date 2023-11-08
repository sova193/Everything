from django.apps import AppConfig
import redis

red = redis.Redis(
    host='redis-19136.c259.us-central1-2.gce.cloud.redislabs.com',
    port=19136,
    password='hgdp0xDZu0oXyVQEDYewdXJjjw1Bo8wc'
)

class SimpleappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'simpleapp'

    def ready(self):
        import simpleapp.signals
