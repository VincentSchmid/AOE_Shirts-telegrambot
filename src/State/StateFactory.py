from enum import Enum

from .Idle import Idle
from .ReceivingShirts import ReceivingShirts
from .ReturningResult import ReturningResult
from .SettingBackground import SettingBackground
from .Help import Help

from ..Model import AppModel


class StateFactory():
    class StateType(Enum):
        IDLE = 0
        SETTING_BACKGROUND = 1
        RECEIVING_SHIRTS = 2
        RETURNING_RESULT = 3
        HELP = 4

    def __init__(self, model: AppModel, options: dict):
        self.model: AppModel = model
        self.options: dict = options

    def get_state(self, stateType: StateType):
        params = [self.model, self.options]
        return {
            stateType.IDLE: Idle,
            stateType.SETTING_BACKGROUND: SettingBackground,
            stateType.RECEIVING_SHIRTS: ReceivingShirts,
            stateType.RETURNING_RESULT: ReturningResult,
            stateType.HELP: Help
        }.get(stateType)(*params)
