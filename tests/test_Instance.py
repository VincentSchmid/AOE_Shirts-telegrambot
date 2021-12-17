from unittest.mock import MagicMock
from pytest_mock import MockerFixture

from src.Model import AppModel
from src.Instance import Instance
from src.Messager import Messager
import src.options as options
from src.State.StateFactory import StateFactory


def test_Instance_event_calls(mocker: MockerFixture):
    test_model: AppModel = AppModel({}, "http:abc.xyz/8000")
    test_options: dict = options.get_options("config.yaml")
    test_state_factory: StateFactory = StateFactory(test_model, test_options)
    test_messager: Messager = Messager(test_model)
    test_messager.send_telegram_message = MagicMock()
    test_messager.send_file = MagicMock()

    test_messager.listen()

    test_instance: Instance = Instance(
        test_model, test_options, test_state_factory, test_messager)

    test_model.events.started()
    test_model.events.background_set()
    test_model.events.shirts_received()
    test_model.events.return_results()
    