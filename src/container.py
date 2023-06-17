import os

from api.base import Api
from image import Image

Env = tuple[str, str]
Option = tuple[str, str]
Port = tuple[int | str, int, str]
Volume = tuple[str, str]

class Container:
  def __init__(self, provider: Api.Container, name: str, image: Image):
    self.__provider = provider
    self.__name = name
    self.__image = image
    self.__envs = []
    self.__ports = []
    self.__volumes = []
    self.__options = []

  def name(self) -> str:
    return self.__name

  def set_env(self, value: Env) -> None:
    self.__envs.append(value)

  def set_volume(self, value: Volume) -> None:
    if not os.path.isdir(value[0]):
      raise Exception(f"Invalid source path: {value[0]}")

    self.__volumes.append(value)

  def set_port(self, value: Port) -> None:
    self.__ports.append(value)

  def set_option(self, value: Option) -> None:
    self.__options.append(value)

  def create(self) -> None:
    envs = [f"-e {key}={value}" for (key, value) in self.__envs]
    volumes = [f"-v {source}:{target}" for (source, target) in self.__volumes]
    ports = [f"-p {source}:{target}/{ptype}" for (source, target, ptype) in self.__ports]
    options = [f"--{name} {value}" for (name, value) in self.__options]

    self.__image.pull()
    self.__provider.create(
      self.name(),
      self.__image.name(),
      [*envs, *volumes, *ports, *options]
    )

  def start(self) -> None:
    self.__provider.start(self.name())

  def stop(self) -> None:
    self.__provider.stop(self.name())

  def delete(self) -> None:
    self.__provider.delete(self.name())
    self.__image.delete()
