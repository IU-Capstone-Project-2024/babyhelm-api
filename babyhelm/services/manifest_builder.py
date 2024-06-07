from functools import cached_property
from pathlib import Path

import jinja2
from jinja2 import Template

from babyhelm.schemas.manifest_builder import Values


class ManifestBuilderService:

    def __init__(self, templates_directory: Path):
        self.template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=templates_directory))

    @cached_property
    def deployment_template(self) -> Template:
        return self.template_env.get_template("deployment.j2")

    @cached_property
    def service_template(self) -> Template:
        return self.template_env.get_template("service.j2")

    def render_deployment_manifest(self, values: Values) -> str:
        return self.deployment_template.render(Values=values)

    def render_service_manifest(self, values: Values) -> str:
        return self.service_template.render(Values=values)
