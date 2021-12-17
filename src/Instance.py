from telegram import Update
from telegram.files.file import File
from telegram.ext import CallbackContext

from .Model import AppModel
from .State.StateFactory import StateFactory
from .State.State import State
from .Messager import Messager
from .ShirtProcessing import full_pipeline
from pathlib import Path


class Instance():
    def __init__(self, model: AppModel, options: dict, state_factory: StateFactory, messager: Messager) -> None:
        self.options: dict = options
        self.model: AppModel = model
        self._state_factory: StateFactory = state_factory
        self._state: State = self._state_factory.get_state(
            StateFactory.StateType.IDLE)
        self._messager: Messager = messager
        self._messager.listen()

        self.model.events.started += self.on_started
        self.model.events.background_set += self.on_background_set
        self.model.events.shirts_received += self.on_shirts_received
        self.model.events.return_results += self.on_return_results

    def on_start_command(self, update: Update, context: CallbackContext):
        self.model.update = update
        self._state.start_handler()

    def on_help_command(self, update: Update, context: CallbackContext):
        self.model.update = update
        self._state = self._state_factory.get_state(
            StateFactory.StateType.HELP)

    def on_done_command(self, update: Update, context: CallbackContext):
        self.model.update = update
        self._state.done_handler()

    def on_document_received(self, update: Update, context: CallbackContext):
        self.model.update = update
        self._state.document_received(update.message.effective_attachment)

    def on_photo_received(self, update: Update, context: CallbackContext):
        self.model.update = update
        self._state.document_received(update.message.effective_attachment[-1])

    def on_started(self):
        self._state = self._state_factory.get_state(
            StateFactory.StateType.SETTING_BACKGROUND)

    def on_background_set(self):
        self._state = self._state_factory.get_state(
            StateFactory.StateType.RECEIVING_SHIRTS)

    def on_shirts_received(self):
        self._state = self._state_factory.get_state(
            StateFactory.StateType.RETURNING_RESULT)

    def on_return_results(self):
        for shirt in self.model.shirts:
            self.process_shirt(
                self.model.background.get_file(), shirt.get_file())
        self._state.done_handler()

    def process_shirt(self, background: File, foreground: File):
        background_filename = Path(background.file_path).name
        foreground_filename = Path(foreground.file_path).name

        background_data = background.download_as_bytearray()
        foreground_data = foreground.download_as_bytearray()

        self.model.result = full_pipeline(
            self.model.url, self.options["PARAMS"]["RESIZE_PERCENTAGE"],
            background_filename, background_data, foreground_filename, foreground_data)
        self._messager.send_file()
