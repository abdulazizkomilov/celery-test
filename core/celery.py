import os

from celery import Celery
from celery.schedules import crontab

from kombu import Queue
# from kombu import Queue, Exchange
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery("config")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

BROKER_URL = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"  # noqa

app.conf.update(
    broker_url=BROKER_URL,
    result_backend=BROKER_URL,
    accept_content=["json"],
    task_serializer="json",
    result_serializer="json",
    task_always_eager=not BROKER_URL,
    task_ignore_result=True,
    task_store_errors_even_if_ignored=True,
    enable_utc=True,
    timezone="Asia/Tashkent",
    broker_connection_retry_on_startup=True,
    task_track_started=True,
    worker_send_task_events=True,
    task_send_sent_event=True,
    broker_transport_options={
        "priority_steps": list(range(10)),
        "queue_order_strategy": "priority",
    },
)

app.conf.task_queues = (
    Queue('default', routing_key='task.#'),
    Queue('sms_queue', routing_key='sms.#'),
)

app.conf.task_routes = {
    'send_message': {
        'queue': 'sms_queue',
        'routing_key': 'sms.send',
        'priority': 0,
    },
}

schedule_crontab = {"schedule": crontab(hour="*/2", minute="0")}

if settings.DEBUG or settings.DEVELOPMENT:
    schedule_crontab = {"schedule": crontab(minute="*/1")}

app.conf.beat_schedule = {
    "auto-write-off-by-schedule": {
        "task": "auto_task_runner",
        # a job is scheduled to run on the every two hours on production
        **schedule_crontab,
    }
}
