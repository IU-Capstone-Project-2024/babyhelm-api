from pydantic import BaseModel


class Service(BaseModel):
    name: str


class App(BaseModel):
    name: str
    image: str
    port: int
    service: Service


class Values(BaseModel):
    app: App
