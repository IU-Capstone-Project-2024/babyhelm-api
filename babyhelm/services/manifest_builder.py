from functools import cached_property
from pathlib import Path

import jinja2
import yaml
from jinja2 import Template

from babyhelm.schemas.manifest_builder import (
    App,
    Application,
    Deployment,
    Manifests,
    Service,
    Values,
)


class ManifestBuilderService:
    def __init__(self, templates_directory: Path):
        self.template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(searchpath=templates_directory)
        )

    @cached_property
    def deployment_template(self) -> Template:
        return self.template_env.get_template("deployment.j2")

    @cached_property
    def service_template(self) -> Template:
        return self.template_env.get_template("service.j2")

    @cached_property
    def hpa_template(self) -> Template:
        return self.template_env.get_template("hpa.j2")

    @staticmethod
    def _make_values(application: Application) -> Values:
        envs = []
        for env in application.envs:
            envs.append({"name": env.name, "value": env.value})
        return Values(
            app=App(
                name=application.name,
                deployment=Deployment(
                    postfix="deployment",
                    replicas=2,
                    image=application.image,
                    port=application.ports.target_port,
                ),
                service=Service(
                    postfix="svc",
                    type="LoadBalancer",
                    loadBalancerClass="tailscale",
                    ports=application.ports,
                ),
                envs=envs,
            )
        )

    def render_application(self, application: Application) -> Manifests:
        values = self._make_values(application)
        deployment = yaml.safe_load(self.deployment_template.render(Values=values))
        service = yaml.safe_load(self.service_template.render(Values=values))
        hpa = yaml.safe_load(self.hpa_template.render(Values=values))
        return Manifests(deployment=deployment, service=service, hpa=hpa)
