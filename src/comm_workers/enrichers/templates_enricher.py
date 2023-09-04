import jinja2

from .abstract import TemplateEnricherABC


class TemplateEnricher(TemplateEnricherABC):
    def __init__(self):
        self.environment = jinja2.Environment()

    def render_template(self, template: str, context: dict) -> str:
        jinja_template = self.environment.from_string(template)
        return jinja_template.render(**context)
