import os

from api.docker import Docker
from api.podman import Podman
from container import Container, Env, Option, Port, Volume
from image import Image

API = os.getenv("API")

class Context:
  @staticmethod
  def PrepareContainer(
    name: str,
    image_name: str,
    command: str | None,
    envs: list[Env] = [],
    volumes: list[Volume] = [],
    ports: list[Port] = [],
    options: list[Option] = []
  ) -> Container:
    provider = Podman
    if API:
      ["docker", "podman"].index(API)
      if API == "docker":
        provider = Docker

    image = Image(provider.Image(), image_name)
    container = Container(provider.Container(), name, image, command)
    for env in envs:
      container.set_env(env)
    for volume in volumes:
      container.set_volume(volume)
    for port in ports:
      container.set_port(port)
    for option in options:
      container.set_option(option)

    return container

  def __init__(self, containers: list[Container]):
    self.__containers = containers

  def create(self) -> None:
    for container in self.__containers:
      container.create()

  def start(self) -> None:
    for container in self.__containers:
      container.start()

  def stop(self) -> None:
    for container in self.__containers:
      container.stop()

  def update(self) -> None:
    for container in self.__containers:
      container.stop()
      container.delete()
      container.create()

  def delete(self) -> None:
    for container in self.__containers:
      container.delete()
