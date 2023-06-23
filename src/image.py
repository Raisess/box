from api.base import Api

class Image:
  def __init__(self, provider: Api.Image, name: str):
    self.__provider = provider
    splitted = name.split(":")
    self.__name = splitted[0]
    self.__version = splitted[1] if len(splitted) > 1 else "latest"

  def name(self) -> str:
    return self.__name

  def version(self) -> str:
    return self.__version

  def pull(self) -> None:
    self.__provider.pull(self.name(), self.version())

  def delete(self) -> None:
    self.__provider.delete(self.name())
