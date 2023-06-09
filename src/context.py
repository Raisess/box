from container import Container
from shell import Shell

class Context:
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
