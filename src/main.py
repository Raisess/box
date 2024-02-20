#! /usr/bin/env python3

import json
import os

from yacli import CLI, Command
from context import Context

class BaseCommand(Command):
  def __init__(self, command: str, description: str, args_len: int):
    super().__init__(command, description, args_len)

  def _init_context(self, args: list[str]) -> Context:
    file_path = args[0]
    container_names = args[1:] if len(args) >= 2 else None
    return self.__handle(file_path, container_names)

  def __handle(self, file_path: str, container_names: list[str] = None) -> Context:
    if not os.path.isfile(file_path):
      raise Exception("Provided file do not exists")
    if not file_path.endswith(".json"):
      raise Exception("Invalid file extesion, try a .json")

    containers = []
    with open(file_path) as file:
      data = json.loads(file.read())
      if type(data) != list:
        raise Exception("Invalid file format")

      if container_names:
        for container_name in container_names:
          for item in data:
            if container_name == item.get("name"):
              containers.append(Context.PrepareContainer(
                name=item.get("name"),
                image_name=item.get("image"),
                command=item.get("command"),
                envs=item.get("envs") or [],
                volumes=item.get("volumes") or [],
                ports=item.get("ports") or [],
                options=item.get("options") or []
              ))
      else:
        for item in data:
          containers.append(Context.PrepareContainer(
            name=item.get("name"),
            image_name=item.get("image"),
            command=item.get("command"),
            envs=item.get("envs") or [],
            volumes=item.get("volumes") or [],
            ports=item.get("ports") or [],
            options=item.get("options") or []
          ))

    if len(containers) == 0:
      raise Exception("No valid containers in the context")

    return Context(containers)


class Create(BaseCommand):
  def __init__(self):
    super().__init__("create", "Create new containers", args_len=1)

  def handle(self, args: list[str]) -> None:
    context = self._init_context(args)
    context.create()


class Start(BaseCommand):
  def __init__(self):
    super().__init__("start", "Start containers", args_len=1)

  def handle(self, args: list[str]) -> None:
    context = self._init_context(args)
    context.start()


class Stop(BaseCommand):
  def __init__(self):
    super().__init__("stop", "Stop containers", args_len=1)

  def handle(self, args: list[str]) -> None:
    context = self._init_context(args)
    context.stop()


class Update(BaseCommand):
  def __init__(self):
    super().__init__("update", "Update containers", args_len=1)

  def handle(self, args: list[str]) -> None:
    context = self._init_context(args)
    context.update()


class Delete(BaseCommand):
  def __init__(self):
    super().__init__("delete", "Delete containers", args_len=1)

  def handle(self, args: list[str]) -> None:
    context = self._init_context(args)
    context.delete()


class Restart(BaseCommand):
  def __init__(self):
    super().__init__("restart", "Restart containers", args_len=1)

  def handle(self, args: list[str]) -> None:
    context = self._init_context(args)
    context.restart()


class Serve(Command):
  def __init__(self):
    super().__init__("serve", "Start an REST API")

  def handle(self, args: list[str]) -> None:
    import uvicorn
    from server import app

    port = args[1] if len(args) > 1 else 8000
    host = args[2] if len(args) > 2 else "localhost"

    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
  cli = CLI("box", [
    Create(),
    Start(),
    Stop(),
    Delete(),
    Update(),
    Restart(),
    Serve()
  ])
  cli.handle()
