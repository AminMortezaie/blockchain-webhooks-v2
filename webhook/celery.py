import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webhook.settings')

app = Celery('webhook')

# Load task modules from little change in btc transactions.m all registered Django app configs.
app.autodiscover_tasks()

# Configure Celery to use Redis as the message broker.
app.conf.broker_url = 'redis://redis:6379/1'


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


app.conf.beat_schedule = {
    'update_wallets_hashmap': {
        'task': 'update_wallets_hashmap',
        'schedule': 500
    },
    'get_blocks_trc20': {
        'task': 'get_blocks_trc20',
        'schedule': 30
    },
}

