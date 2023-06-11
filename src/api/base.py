class Api:
  class Container:
    def create(self, name: str, image: str, args: list[str]) -> None:
      raise NotImplemented()

    def delete(self, name: str) -> None:
      raise NotImplemented()


  class Image:
    def pull(self, name: str, version: str) -> None:
      raise NotImplemented()

    def delete(self, name: str) -> None:
      raise NotImplemented()
