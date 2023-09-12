import jinja2
import nh3
import tidylib

from .abstract import TemplateEnricherABC


class TemplateEnricher(TemplateEnricherABC):
    def __init__(self):
        self.environment = jinja2.Environment()
        self.validator = tidylib.Tidy()

    def validate_and_clean_template(self, template: str):
        document = self.validator.tidy_document(template)
        return nh3.clean(document[0])

    def render_template(self, template: str, context: dict) -> str:
        jinja_template = self.environment.from_string(template)
        rendered = jinja_template.render(**context)
        return self.validate_and_clean_template(rendered)
