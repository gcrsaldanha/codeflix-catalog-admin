rabbitstart:
	docker run -d --hostname rabbitmq --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management

rabbitstop:
	docker stop rabbitmq
	docker rm rabbitmq

run:
	python manage.py runserver

shell:
	python manage.py shell_plus
