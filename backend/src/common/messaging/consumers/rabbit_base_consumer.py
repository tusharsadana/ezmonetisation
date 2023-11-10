# stdlib
import abc
import asyncio
import logging
import traceback
import typing
from multiprocessing import Manager, Process, Queue

# thirdparty
import pydantic
from aio_pika.abc import ExchangeType

# project
from src.common.messaging.rabbit_base import RabbitClient
from src.common.utils import log_ram_usage

logger = logging.getLogger(__name__)


class RabbitConsumerFabric(RabbitClient, abc.ABC):
    def __init__(self, prefetch_count: int):
        self.prefetch_count = prefetch_count
        self.channel = None

    async def execute_in_process(
        self, func: typing.Callable, *args, **kwargs
    ) -> typing.Any:
        """
        Self-written async wrapper for starting
        task in process and periodically
        check status.

        When execute in process pool returns 135 exit status.
        """

        def __run_in_process(
            function: typing.Callable,
            queue: Queue,
            *args_inner,
            **kwargs_inner
        ) -> None:
            """
            Wrapper for run function and
            store results in queue.
            """
            queue.put_nowait(function(*args_inner, **kwargs_inner))

        q = Manager().Queue()
        process = Process(
            target=__run_in_process, args=(func, q, *args), kwargs=kwargs
        )
        process.start()
        while process.is_alive():
            await asyncio.sleep(1)
            if q.qsize() == 1:
                process.terminate()

        return q.get_nowait()

    @property
    @abc.abstractmethod
    def msg_model(self) -> typing.Type[pydantic.BaseModel]:
        """Message data model type"""

    @abc.abstractmethod
    async def main_action(self, msg, *args, **kwargs):
        """Actions related to received message"""

    @staticmethod
    async def validation_error_handling():
        """Validation error handling"""
        logger.error(traceback.format_exc())

    def parse_message(self, message: bytes) -> pydantic.BaseModel:
        """Method for message parsing"""
        return self.msg_model.parse_raw(message)

    async def consume(self, loop: asyncio.AbstractEventLoop, *args, **kwargs):
        async with self.connection(loop=loop) as connection:
            self.channel = await connection.channel()

            await self.channel.set_qos(prefetch_count=self.prefetch_count)

            exchange = await self.channel.declare_exchange(
                self.exchange, type=ExchangeType.DIRECT, durable=True
            )
            queue = await self.channel.declare_queue(self.queue, durable=True)
            await queue.bind(exchange, routing_key=self.queue)

            logger.info(
                "%s: start consuming messages from %s"
                % (self.__class__.__name__, self.queue)
            )

            async with queue.iterator() as queue_iter:
                async for msg in queue_iter:
                    async with msg.process():
                        # parsing part
                        logger.info(
                            "%s: message received" % self.__class__.__name__
                        )
                        log_ram_usage()
                        try:
                            parsed_msg = self.parse_message(message=msg.body)
                        except pydantic.ValidationError:
                            await self.validation_error_handling()
                            continue

                        # postprocessing part
                        try:
                            await self.main_action(msg=parsed_msg)
                        except Exception as e:
                            await self.handle_error(error=e, msg=parsed_msg)

    @staticmethod
    async def handle_error(error, msg, *args, **kwargs):
        logger.exception("Could not consume message %s" % error)
