from api.base import Api
from util.shell import Shell

class Docker(Api):
  class Container(Api.Container):
    def create(self, name: str, image: str, args: list[str]) -> None:
      Shell.Execute(f"docker container create --name {name} {' '.join(args)} {image}")

    def delete(self, name: str) -> None:
      Shell.Execute(f"docker container rm {name}")

    def start(self, name: str) -> None:
      Shell.Execute(f"docker container start {name}")

    def stop(self, name: str) -> None:
      Shell.Execute(f"docker container stop {name}")


  class Image(Api.Image):
    def pull(self, name: str, version: str) -> None:
      Shell.Execute(f"docker image pull {name}:{version}")

    def delete(self, name: str) -> None:
      Shell.Execute(f"docker image rm {name}")
