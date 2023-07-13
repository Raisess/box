from api.base import Api
from util.shell import Shell

class Podman(Api):
  class Container(Api.Container):
    def create(self, name: str, image: str, command: str, args: list[str]) -> None:
      Shell.ExecuteTTY(f"podman container create --name {name} {' '.join(args)} {image} {command}")

    def delete(self, name: str) -> None:
      Shell.ExecuteTTY(f"podman container rm -v {name}")

    def start(self, name: str) -> None:
      Shell.ExecuteTTY(f"podman container start {name}")

    def stop(self, name: str) -> None:
      Shell.ExecuteTTY(f"podman container stop {name}")

    def logs(self, name: str, args: list[str]) -> str:
      return Shell.Execute(f"podman container logs {' '.join(args)} {name}")

    def inspect(self, name: str) -> dict:
      import json
      data = json.loads(Shell.Execute(f"podman container inspect {name}"))
      return data[0]


  class Image(Api.Image):
    def pull(self, name: str, version: str) -> None:
      Shell.ExecuteTTY(f"podman image pull {name}:{version}")

    def delete(self, name: str) -> None:
      Shell.ExecuteTTY(f"podman image rm {name}")
