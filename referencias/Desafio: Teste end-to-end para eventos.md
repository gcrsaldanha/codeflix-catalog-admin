# Desafio: Teste End-to-End para Eventos

Escreva um teste end-to-end que realiza os seguintes passos:

1. Cria uma instância de Category, Genre e CastMember utilizando as respectivas APIs.
2. Cria um Video utiilzando a respectiva API.
3. Faz o upload de uma mídia utilizando a API.
4. Publica um evento na fila `videos.converted`.
   1. Você vai precisar rodar o RabbitMQ Server e o Consumer para isso:
```bash
# Inicializar o docker com RabbitMQ Server
docker run -d --hostname rabbitmq --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management

# Inicializar o consumer
python manage.py startconsumer
```
   2. Utilize esse [código de exemplo](../code_examples/send_message_to_rabbit_mq.py) para enviar uma mensagem para a fila `videos.converted`.
   3. Lembre-se de atualizar a mensagem de exemplo com o ID do Video entity correto.
6. Verifique que o `video.video` (`AudioVideoMedia`) foi devidamente processado.
   1. Ou seja, `MediaStatus.COMPLETED`.
   2. Caso você já tenha a API para buscar detalhes de um `Video`, pode utilizá-la para isso. Caso contrário, faça uma consulta no banco mesmo para confirmar o status.
