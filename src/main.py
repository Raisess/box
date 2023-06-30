#! /usr/bin/env python3

import json
import os

from yacli import CLI, Command
from context import Context

def init_context(file_path: str, container_name: str | None) -> Context:
  if not os.path.isfile(file_path):
    raise Exception("Provided file do not exists")
  if not file_path.endswith(".json"):
    raise Exception("Invalid file extesion, try a .json")

  containers = []
  with open(file_path) as file:
    data = json.loads(file.read())
    if type(data) != list:
      raise Exception("Invalid file format")

    if container_name:
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
          continue
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


class Create(Command):
  def __init__(self):
    super().__init__("create", "Create new containers", args_len=1)

  def handle(self, args: list[str]) -> None:
    file_path = args[0]
    container_name = args[1] if len(args) > 1 else None
    context = init_context(file_path, container_name)
    context.create()


class Start(Command):
  def __init__(self):
    super().__init__("start", "Start containers", args_len=1)

  def handle(self, args: list[str]) -> None:
    file_path = args[0]
    container_name = args[1] if len(args) > 1 else None
    context = init_context(file_path, container_name)
    context.start()


class Stop(Command):
  def __init__(self):
    super().__init__("stop", "Stop containers", args_len=1)

  def handle(self, args: list[str]) -> None:
    file_path = args[0]
    container_name = args[1] if len(args) > 1 else None
    context = init_context(file_path, container_name)
    context.stop()


class Update(Command):
  def __init__(self):
    super().__init__("update", "Update containers", args_len=1)

  def handle(self, args: list[str]) -> None:
    file_path = args[0]
    container_name = args[1] if len(args) > 1 else None
    context = init_context(file_path, container_name)
    context.update()


class Delete(Command):
  def __init__(self):
    super().__init__("delete", "Delete containers", args_len=1)

  def handle(self, args: list[str]) -> None:
    file_path = args[0]
    container_name = args[1] if len(args) > 1 else None
    context = init_context(file_path, container_name)
    context.delete()


class Restart(Command):
  def __init__(self):
    super().__init__("restart", "Restart containers", args_len=1)

  def handle(self, args: list[str]) -> None:
    file_path = args[0]
    container_name = args[1] if len(args) > 1 else None
    context = init_context(file_path, container_name)
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
  cli = CLI("box", [Create(), Start(), Stop(), Delete(), Update(), Restart(), Serve()])
  cli.handle()
