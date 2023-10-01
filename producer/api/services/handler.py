from aiohttp import web
import logging


class Handler():

    def __init__(self, rabbitmq) -> None:
        self.rabbitmq = rabbitmq

    async def publish(self, request):
        logging.info("Call publish... ")
        body = await request.json()
        self.rabbitmq.publish(message={"data": body})
        return web.json_response({'message': body})

