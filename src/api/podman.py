from api.base import Api
from util.shell import Shell

class Podman(Api):
  class Container(Api.Container):
    def create(self, name: str, image: str, args: list[str]) -> None:
      Shell.Execute(f"podman container create --name {name} {' '.join(args)} {image}")

    def delete(self, name: str) -> None:
      Shell.Execute(f"podman container rm {name}")


  class Image(Api.Image):
    def pull(self, name: str, version: str) -> None:
      Shell.Execute(f"podman image pull {name}:{version}")

    def delete(self, name: str) -> None:
      Shell.Execute(f"podman image rm {name}")
