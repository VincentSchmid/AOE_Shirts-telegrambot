import os

from fastapi import FastAPI, Request, status
from werkzeug.wrappers import Response

from src.State.StateFactory import StateFactory
from src.InstanceHandler import InstanceHandler
from src.Messager import Messager
import src.options as options

from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, Filters, MessageHandler


TELEGRAM_TOKEN = os.environ["TOKEN"]
CONFIG_FILENAME = "config.yaml" if "CONFIG_FILE" not in os.environ else os.environ[
    "CONFIG_FILE"]
SHIRT_PROCESSING_ADDRESS = os.environ["SHIRT_POROCESSING_ADDRESS"]

app = FastAPI()
bot = Bot(token=TELEGRAM_TOKEN)

app_options = options.get_options(CONFIG_FILENAME)
app_state_factory = StateFactory(app_options)
app_messager = Messager(bot)

app_instance_handler = InstanceHandler(SHIRT_PROCESSING_ADDRESS,
                                  app_options,
                                  app_state_factory,
                                  app_messager,
                                  bot)

def start_handler(update, context):
    app_instance_handler.get_instance(update.message.chat_id).on_start_command(update, context)

def done_handler(update, context):
    app_instance_handler.get_instance(update.message.chat_id).on_done_command(update, context)

def help_handler(update, context):
    app_instance_handler.get_instance(update.message.chat_id).on_help_command(update, context)

def document_handler(update, context):
    app_instance_handler.get_instance(update.message.chat_id).on_document_received(update, context)

def photo_handler(update, context):
    app_instance_handler.get_instance(update.message.chat_id).on_photo_received(update, context)

dispatcher = Dispatcher(bot=bot, update_queue=None)

dispatcher.add_handler(CommandHandler(app_options["COMMANDS"]["START"], start_handler))
dispatcher.add_handler(CommandHandler(app_options["COMMANDS"]["DONE"], done_handler))
dispatcher.add_handler(CommandHandler(app_options["COMMANDS"]["HELP"], help_handler))
dispatcher.add_handler(MessageHandler(Filters.document, document_handler))
dispatcher.add_handler(MessageHandler(Filters.photo, photo_handler))

@app.post("/")
async def index(request: Request) -> Response:
    req_json = await request.json()

    dispatcher.process_update(
        Update.de_json(req_json, bot))

    return Response(status = status.HTTP_204_NO_CONTENT)
