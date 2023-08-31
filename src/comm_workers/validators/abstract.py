from abc import ABC, abstractmethod

from pydantic import BaseModel


class ValidatorABC(ABC):
    @abstractmethod
    def validate_for_send(self, msg: dict) -> BaseModel | None:
        """
        check if the message from the broker is valid for the
        current channel
        """
        raise NotImplementedError

    @abstractmethod
    def validate_for_sender(self, msg: dict) -> object | None:
        """
        check if the message from the broker is valid for the
        current channel, then - valid for the channel's sender
        """
        self.validate_for_send(msg)
