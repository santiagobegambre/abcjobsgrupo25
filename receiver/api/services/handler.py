from aiohttp import web
import logging


class Handler():

    def __init__(self, rabbitmq) -> None:
        self.rabbitmq = rabbitmq

    async def receiver(self, request):
        logging.info("Call receiver... ")
        quees=self.rabbitmq.get_messages()
        logging.info(quees)
        return web.Response(text='successful message receiver')
