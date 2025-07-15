#!/usr/bin/make

run:
	python manage.py runserver

make:
	python manage.py makemigrations

migrate:
	python manage.py migrate

create:
	python manage.py createsuperuser

shell:
	python manage.py shell

worker:
	celery \
		-A core worker \
		--loglevel INFO \
		--queues default \
		--hostname=default_worker@%h \
		-P gevent \
		-c 1000

worker-sms:
	celery \
		-A core worker \
		--loglevel INFO \
		--queues sms_queue \
		--hostname=sms_worker@%h \
		-P gevent \
		-c 1000

flower:
	celery \
        -A core \
        --broker="redis://localhost:6379/0" \
        flower \
        --address=0.0.0.0 \
        --port=5555 \
        --url_prefix=flower \
        --loglevel INFO \
        --basic-auth=login:password \
        --persistent=True

beat:
	celery -A core beat --loglevel INFO --max-interval=15
