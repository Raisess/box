from image import Image
from shell import Shell

Env = tuple[str, str]
Volume = tuple[str, str]
Port = tuple[int, int, str]
Option = tuple[str, str]

class Container:
  @staticmethod
  def Open(
    name: str,
    image_name: str,
    envs: list[Env] = None,
    volumes: list[Volume] = None,
    ports: list[Port] = None,
    options: list[Option] = None
  ) -> "Container":
    container = Container(name, Image(image_name))

    if envs:
      for env in envs:
        container.set_env(env)
    if volumes:
      for volume in volumes:
        container.set_volume(volume)
    if ports:
      for port in ports:
        container.set_port(port)
    if options:
      for option in options:
        container.set_option(option)

    return container

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
    self.__volumes.append(value)

  def set_port(self, value: Port) -> None:
    self.__ports.append(value)

  def set_option(self, value: Option) -> None:
    self.__options.append(value)

  def create(self) -> None:
    envs = [f"-e {key}={value}" for (key, value) in self.__envs]
    volumes = [f"-v {source}:{target}" for (source, target) in self.__volumes]
    ports = [f"-p {source}:{target}/{ptype}" for (source, target, ptype) in self.__ports]
    options = [f"--{name}:{value}" for (name, value) in self.__options]

    self.__image.pull()
    Shell.Execute(f"""
      podman container create --name {self.__name} \
      {" ".join(envs)} \
      {" ".join(volumes)} \
      {" ".join(ports)} \
      {self.__image.name()}
    """)

  def delete(self) -> None:
    Shell.Execute(f"podman container rm {self.__name}")
    self.__image.delete()

  def update(self) -> None:
    self.delete()
    self.__image.pull()
    self.create()
