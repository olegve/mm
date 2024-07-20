from api.services.message import APIDataHandler
from core.input_channel import InputChannelChoice
from core.input_data_handler import AbstractInputDataHandler


class InputDataHandler:
    """Фабрика, определяющая конвертер входных данных"""
    @classmethod
    def make(cls, channel: InputChannelChoice) -> AbstractInputDataHandler:
        """Метод, определяющий конвертер входных данных в Message на основании типа входного канала"""
        match channel:
            case InputChannelChoice.API_MESSAGE:
                return APIDataHandler()
            case _:
                return AbstractInputDataHandler()