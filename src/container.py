import os

from image import Image
from shell import Shell

Env = tuple[str, str]
Volume = tuple[str, str]
Port = tuple[int, int, str]
Option = tuple[str, str]

class Container:
  def __init__(self, name: str, image: Image):
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
    Shell.Execute(f"""
      podman container create --name {self.__name} \
      {" ".join(envs)} \
      {" ".join(volumes)} \
      {" ".join(ports)} \
      {" ".join(options)} \
      {self.__image.name()}
    """)

  def delete(self) -> None:
    Shell.Execute(f"podman container rm {self.__name}")
    self.__image.delete()
