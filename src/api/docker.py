from api.base import Api
from util.shell import Shell

class Docker(Api):
  class Container(Api.Container):
    def create(self, name: str, image: str, command: str, args: list[str]) -> None:
      Shell.ExecuteTTY(f"docker container create --name {name} {' '.join(args)} {image} {command}")

    def delete(self, name: str) -> None:
      Shell.ExecuteTTY(f"docker container rm {name}")

    def start(self, name: str) -> None:
      Shell.ExecuteTTY(f"docker container start {name}")

    def stop(self, name: str) -> None:
      Shell.ExecuteTTY(f"docker container stop {name}")

    def logs(self, name: str, args: list[str]) -> str:
      return Shell.Execute(f"docker container logs {' '.join(args)} {name}")

    def stats(self, name: str) -> dict:
      import json
      data = json.loads(Shell.Execute(f"docker container stats {name} --format=json --no-stream"))
      return data[0]

    def inspect(self, name: str) -> dict:
      import json
      data = json.loads(Shell.Execute(f"docker container inspect {name}"))
      return data[0]

  class Image(Api.Image):
    def pull(self, name: str, version: str) -> None:
      Shell.ExecuteTTY(f"docker image pull {name}:{version}")

    def delete(self, name: str) -> None:
      Shell.ExecuteTTY(f"docker image rm {name}")
