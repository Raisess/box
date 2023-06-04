from image import Image
from shell import Shell

Env = tuple[str, str]
Volume = tuple[str, str]
Port = tuple[int, int, str]

class Container:
  @staticmethod
  def Open(
    name: str,
    image_name: str,
    envs: list[Env] = [],
    volumes: list[Volume] = [],
    ports: list[Port] = []
  ) -> "Container":
    container = Container(name, Image(image_name))
    for env in envs:
      container.set_env(env)
    for volume in volumes:
      container.set_volume(volume)
    for port in ports:
      container.set_port(port)

    return container

  def __init__(self, name: str, image: Image):
    self.__name = name
    self.__image = image
    self.__envs = []
    self.__ports = []
    self.__volumes = []

  def name(self) -> str:
    return self.__name

  def set_env(self, value: Env) -> None:
    self.__envs.append(value)

  def set_volume(self, value: Volume) -> None:
    self.__volumes.append(value)

  def set_port(self, value: Port) -> None:
    self.__ports.append(value)

  def create(self) -> None:
    envs = [f"{env[0]}={env[1]}" for env in self.__envs]
    volumes = [f"{volume[0]}:{volume[1]}" for volume in self.__volumes]
    ports = [f"{port[0]}:{port[1]}/{port[2]}" for port in self.__ports]

    self.__image.pull()
    Shell.Execute(f"""
      podman container create --name {self.__name} \
      {"-e ".join(envs)} \
      {"-v ".join(volumes)} \
      {"-p ".join(ports)} \
      {self.__image.name()}
    """)

  def delete(self) -> None:
    Shell.Execute(f"podman container rm {self.__name}")
    self.__image.delete()

  def update(self) -> None:
    self.delete()
    self.__image.pull()
    self.create()
