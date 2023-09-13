from core.loggers import LOGGER
from enrichers.abstract import TemplateEnricherABC
from senders.abstract import SenderABC
from storages.abstract import StorageABC
from validators.abstract import ValidatorABC

from .abstract import ChannelABC


class EmailChannel(ChannelABC):
    def __init__(
        self,
        sender: SenderABC,
        validator: ValidatorABC,
        storage: StorageABC,
        enricher: TemplateEnricherABC,
    ):
        self.sender = sender
        self.validator = validator
        self.storage = storage
        self.enricher = enricher

    async def handle_message(self, msg: dict) -> None | Exception:
        try:
            template_id = msg.pop("template_id")
        except KeyError as e:
            LOGGER.error("There is no template_id in message %s", msg)
            return e
        try:
            template = await self.storage.get_item(template_id)
        except Exception as e:
            LOGGER.error(
                "Could not get template_body for the message %s with exception", msg, e
            )
            return e
        try:
            message_context = msg.pop("context")
        except KeyError as e:
            LOGGER.error("There is no context for the message %s", msg)
            return e
        try:
            rendered_message = self.enricher.render_template(template, message_context)
        except Exception as e:
            LOGGER.error(
                "Could not render template for the message %s with exception %s ",
                msg,
                e,
            )
            return e
        msg["message"] = rendered_message
        try:
            validated_messages = self.validator.validate_for_sender(msg)
        except Exception as e:
            LOGGER.error("Could not validate the message %s with exception: %s", msg, e)
            return e
        if not isinstance(validated_messages, Exception):
            return await self.sender.send(validated_messages)
        return validated_messages
