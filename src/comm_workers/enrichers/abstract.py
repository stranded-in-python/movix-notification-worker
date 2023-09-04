from abc import ABC, abstractmethod


class TemplateEnricherABC(ABC):
    @abstractmethod
    def render_template(self, template: str, context: dict) -> str:
        raise NotImplementedError
