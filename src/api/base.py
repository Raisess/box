class Api:
  class Container:
    def create(self, name: str, image: str, command: str, args: list[str]) -> None:
      raise NotImplemented()

    def delete(self, name: str) -> None:
      raise NotImplemented()

    def start(self, name: str) -> None:
      raise NotImplemented()

    def stop(self, name: str) -> None:
      raise NotImplemented()

    def inspect(self, name: str) -> dict:
      raise NotImplemented()


  class Image:
    def pull(self, name: str, version: str) -> None:
      raise NotImplemented()

    def delete(self, name: str) -> None:
      raise NotImplemented()
