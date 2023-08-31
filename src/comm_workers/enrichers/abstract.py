from abc import ABC, abstractmethod


class TemplateEnricherABC(ABC):
    @abstractmethod
    def render_template(template: str, context: dict) -> str:
        NotImplemented
