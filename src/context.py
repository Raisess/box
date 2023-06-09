from container import Container
from shell import Shell

class Context:
  def __init__(self, name: str, network: str | None, containers: list[Container]):
    self.__name = name
    self.__network = network
    self.__containers = containers

  def create(self) -> None:
    if self.__network:
      Shell.Execute(f"podman network create {self.__network}")

    for container in self.__containers:
      container.set_option(("net", self.__network))
      container.create()

  def update(self) -> None:
    for container in self.__containers:
      container.delete()
      container.set_option(("net", self.__network))
      container.create()

  def delete(self) -> None:
    for container in self.__containers:
      container.delete()

    if self.__network:
      Shell.Execute(f"podman network rm {self.__network}")
