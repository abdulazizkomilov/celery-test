import logging
import random
import json
import os

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

    # Define file path
    output_file = "sms_responses.json"

    # Check if file exists and read existing data
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # Append the new response
    data.append({"response": response})

    # Write updated data back to the file
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

    return response


@app.task(name="task_1", queue="default", routing_key="task.task1")
def task_1(num):
    logging.info("Task 1 Done: %s", num)


@app.task(name="print_hello", queue="default", routing_key="task.print_hello")
def print_hello(_id):
    logging.info("👋 Hello from custom scheduled task id: %s", _id)


@app.task(name="main_autopay", queue="default", routing_key="task.main_autopay")
def main_autopay():
    today_date = timezone.now().date()

    q_expression = Q(status=False) | Q(date__date__lte=today_date, status__isnull=True)

    schedules = (
        Schedule.objects.annotate(
            payment_amount=F("amount") - F("paid_amount")
        )
        .filter(q_expression)
    )

    logging.info(f"🔁 Found {schedules.count()} schedules to auto write-off.")

    for schedule in schedules:
        try:
            print_hello.delay(schedule.id)
        except Exception as e:
            logging.error(f"❌ Failed to dispatch print_hello for Schedule {schedule.id}: {e}")
