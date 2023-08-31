import jinja2

from .abstract import TemplateEnricherABC


class TemplateEnricher(TemplateEnricherABC):
    def __init__(self):
        self.environment = jinja2.Environment()

    def render_template(self, template: str, context: dict) -> str:
        template = self.environment.from_string(template)
        return template.render(**context)
