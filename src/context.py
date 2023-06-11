from container import Container
from image import Image

class Context:
  @staticmethod
  def PrepareContainer(
    name: str,
    image_name: str,
    envs: list[Env] = [],
    volumes: list[Volume] = [],
    ports: list[Port] = [],
    options: list[Option] = []
  ) -> Container:
    container = Container(name, Image(image_name))
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

  def update(self) -> None:
    for container in self.__containers:
      container.delete()
      container.create()

  def delete(self) -> None:
    for container in self.__containers:
      container.delete()
