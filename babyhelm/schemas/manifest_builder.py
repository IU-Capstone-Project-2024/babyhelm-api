import re

from pydantic import BaseModel, Field, field_validator


class Ports(BaseModel):
    port: int = Field(examples=[80], ge=1, le=65_535)
    target_port: int = Field(alias="targetPort", examples=[80], ge=1, le=65_535)


class Deployment(BaseModel):
    postfix: str
    replicas: int
    image: str
    port: int


class Service(BaseModel):
    postfix: str
    type: str
    load_balancer_class: str = Field(alias="loadBalancerClass")
    ports: Ports


class Env(BaseModel):
    name: str = Field(examples=["config_path"], min_length=1, max_length=128, pattern=r"^[^{}\[\]:*&^%$#@!~`']+$")
    value: str = Field(examples=["Users/admin/config/path"], min_length=1, max_length=1024,
                       pattern=r"^[^{}\[\]:*&^%$#@!~`']+$")


class App(BaseModel):
    name: str
    deployment: Deployment
    service: Service
    envs: list[dict]


class Values(BaseModel):
    app: App


class ApplicationManifests(BaseModel):
    deployment: dict
    service: dict
    hpa: dict


class NamespaceManifest(BaseModel):
    namespace: dict


class Project(BaseModel):
    """
    Project data provided by user
    """
    name: str = Field(max_length=253, examples=["My-project1", "my-awesome-project"], pattern=r"^[a-zA-Z0-9-]+$")


class Application(BaseModel):
    """
    App data provided by user
    """

    name: str = Field(
        max_length=128,
        examples=["sunflower", "snowflake"],
        pattern=r"^[^{}\[\]:,*&^%$#@!~`\"']+$",
    )
    image: str = Field(
        max_length=2048,
        examples=["nginx"],
        pattern=r"^[^{}\[\]*&^%$#@!~`']+$",
    )
    ports: Ports
    envs: list[Env]
