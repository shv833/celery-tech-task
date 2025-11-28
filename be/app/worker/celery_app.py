import os

from celery import Celery

BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
BACKEND_URL = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

celery_app = Celery(
    "worker",
    broker=BROKER_URL,
    backend=BACKEND_URL,
    include=["worker.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    enable_utc=True,
)

celery_app.conf.beat_schedule = {
    "fetch-users-every-30-seconds": {
        "task": "fetch_users_task",
        "schedule": 30.0,
    },
    "enrich-addresses-every-45-seconds": {
        "task": "enrich_address_task",
        "schedule": 45.0,
    },
    "enrich-cc-every-60-seconds": {
        "task": "enrich_cc_task",
        "schedule": 60.0,
    },
}
