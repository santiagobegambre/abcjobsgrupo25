import logging
from aiohttp import web

from api.enums import EnvironmentVariables
from api.gateway.rabbitmq import rabbitMQServer
from api.services.handler import Handler

def main():
    logging.basicConfig(
        format='%(asctime)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO
    )

    server = rabbitMQServer(
        queue=EnvironmentVariables.RABBITMQ_QUEUE.get_env(),
        host=EnvironmentVariables.RABBITMQ_HOST.get_env(),
        routing_key=EnvironmentVariables.RABBITMQ_ROUTING_KEY.get_env(),
        username=EnvironmentVariables.RABBITMQ_USERNAME.get_env(),
        password=EnvironmentVariables.RABBITMQ_PASSSWORD.get_env(),
        exchange=EnvironmentVariables.RABBITMQ_EXCHANGE.get_env(),
    )
    
    app = web.Application()
    handler = Handler(server)

    app.add_routes([
        web.get('/', handler.receiver),
    ])

    web.run_app(
        app,
        port=8000
    )

   
