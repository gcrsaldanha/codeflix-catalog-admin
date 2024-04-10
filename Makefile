startconsumer:
	@if [ -z "`docker ps -q -f name=rabbitmq`" ]; then \
		docker run -d --hostname rabbitmq --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management; \
		sleep 5; \
	fi
	python manage.py startconsumer

stopconsumer:
	docker stop rabbitmq
	docker rm rabbitmq

migrate:
	python manage.py makemigrations && python manage.py migrate

run:
	python manage.py runserver

shell:
	python manage.py shell_plus
