from pydantic import BaseModel, Field, field_validator

import re


class Ports(BaseModel):
    port: int
    target_port: int = Field(alias="targetPort")


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
    name: str
    value: str


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
    name: str = Field(..., max_length=253)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not re.match(r"^[a-zA-Z0-9-]+$", v):
            raise ValueError(
                "Name must contain only alphanumeric characters and hyphens."
            )
        return v


class Application(BaseModel):
    """
    Class for user-side interaction.
    """

    name: str
    image: str
    ports: Ports
    envs: list[Env]

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        forbidden_symbols = "{}[]:,*&^%$#@!~`\"'"
        if any(symb in v for symb in forbidden_symbols):
            raise ValueError(
                f"Name should not contain forbidden symbols: {forbidden_symbols}"
            )
        return v

    @field_validator("image")
    @classmethod
    def validate_image(cls, v):
        forbidden_symbols = "{}[]*&^%$#@!~`'"
        if any(symb in v for symb in forbidden_symbols):
            raise ValueError(
                f"Image should not contain forbidden symbols: {forbidden_symbols}"
            )
        return v

    @field_validator("envs")
    @classmethod
    def validate_envs(cls, v):
        forbidden_symbols = "{}[]:*&^%$#@!~`'"
        for env in v:
            if any(symb in env.name or symb in env.value for symb in forbidden_symbols):
                raise ValueError(
                    f"Env name/value should not contain forbidden symbols: {forbidden_symbols}"
                )
        return v
