from unittest.mock import MagicMock
from events.events import Events
from pytest_mock import MockerFixture

from src.Model import AppModel
from src.Instance import Instance
from src.Messager import Messager
import src.options as options
from src.State.StateFactory import StateFactory


def test_Instance_event_calls(mocker: MockerFixture):
    class MockBot():
        def send_message(*args):
            pass
    
    test_bot = MockBot()
    test_bot.send_message = MagicMock()
    test_events = Events()

    test_model: AppModel = AppModel(test_bot, test_events, "http:abc.xyz/8000")
    test_options: dict = options.get_options("config.yaml")
    test_state_factory: StateFactory = StateFactory(test_model, test_options)
    test_messager: Messager = Messager(test_bot)

    test_instance: Instance = Instance(
        test_model, test_options, test_state_factory, test_messager)

    test_model.events.started()
    test_model.events.background_set()
    test_model.events.shirts_received()
    test_model.events.return_results()
    