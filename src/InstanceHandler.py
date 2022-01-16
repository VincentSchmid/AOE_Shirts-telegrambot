import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from telegram import Bot
from events.events import Events

from .Instance import Instance
from .Model import AppModel
from .State.StateFactory import StateFactory
from .Messager import Messager


class InstanceHandler():
    def __init__(self, processing_url: str, options: dict, state_factory: StateFactory, messager: Messager, bot: Bot) -> None:
        self.options = options
        self.state_factory = state_factory
        self.messager = messager
        self.bot = bot
        self.processing_url = processing_url
        self.instances = {}

        sched = AsyncIOScheduler()
        sched.add_job(self._cleanup_instances, 'interval',
                      seconds=self.options["PARAMS"]["INSTANCE_LIFETIME"]+1)

    def get_instance(self, chat_id: int) -> Instance:
        if chat_id not in self.instances:
            self.instances[chat_id] = (self._create_instance(), time.time())

        instance, _ = self.instances[chat_id]
        self.instances[chat_id] = (instance, time.time())
        
        return instance

    def _create_instance(self) -> Instance:
        events = Events()
        model = AppModel(self.bot, events, self.processing_url)
        return Instance(model, self.options, self.state_factory, self.messager)

    def _cleanup_instances(self):
        for chat_id, (_, timestamp) in self.instances.items():
            if time.time() - timestamp > self.options["PARMAS"]["INSTANCE_LIFETIME"]:
                self.instances.pop(chat_id)
