import logging
import random
import json
import os

from django.db import transaction
from django.utils import timezone
from django.db.models import (
    Case,
    CharField,
    F,
    Q,
    When,
)
from .models import Schedule
from core.celery import (
    app,
)


@app.task(name="send_message", queue="sms_queue", routing_key="sms.send")
def send_sms():
    response = random.randint(100000, 999999)
    output_file = "sms_responses.json"

    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append({"response": response})

    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

    return response


@app.task(name="task_1", queue="default", routing_key="task.task1")
def task_1(num):
    logging.info("Task 1 Done: %s", num)


@app.task(name="process_schedule", queue="default", routing_key="task.process_schedule")
def process_schedule(_id):
    logging.info("Scheduled task id: %s", _id)

    try:
        with transaction.atomic():
            schedule = Schedule.objects.get(id=_id)
            schedule.status = True
            schedule.description = "This is a description: {}".format(_id)
            schedule.save(update_fields=["status", "description"])
            logging.info(f"✅ Updated Schedule {_id}")
    except Schedule.DoesNotExist:
        logging.error(f"❌ Schedule with id {_id} not found")
    except Exception as e:
        logging.error(f"❌ Failed to update status for Schedule {_id}: {e}")


@app.task(name="auto_task_runner", queue="default", routing_key="task.auto_task_runner")
def auto_task_runner():
    today_date = timezone.now().date()

    q_expression = Q(status=False) | Q(date__date__lte=today_date, status__isnull=True)

    schedules = (
        Schedule.objects.filter(q_expression)
    )
    logging.info(f"🔁 Found {schedules.count()} schedules to auto run task.")

    for schedule in schedules:
        try:
            process_schedule.delay(schedule.id)
        except Exception as e:
            logging.error(f"❌ Failed to dispatch process_schedule for Schedule {schedule.id}: {e}")
