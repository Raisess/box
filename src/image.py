from api.base import Api

class Image:
  def __init__(self, provider: Api.Image, name: str):
    self.__provider = provider
    self.__name = name

  def name(self) -> str:
    return self.__name

  def pull(self) -> None:
    self.__provider.pull(self.__name, "latest")

  def delete(self) -> None:
    self.__provider.delete(self.__name)
