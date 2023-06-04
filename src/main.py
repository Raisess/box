#! /usr/bin/env python3

import json
import os

from yacli import CLI, Command
from container import Container

def init_container(file_path: str) -> Container:
  if not file_path.endswith(".json"):
    raise Exception("Invalid file extesion, try a .json")
  if not os.path.isfile(file_path):
    raise Exception("Provided file do not exists")

  container: Container
  with open(file_path) as file:
    data = json.loads(file.read())
    container = Container.Init(
      name=data.get("name") or [],
      image_name=data.get("image") or [],
      envs=data.get("envs") or [],
      volumes=data.get("volumes") or [],
      ports=data.get("ports") or [],
      options=data.get("options") or []
    )

  return container


class Create(Command):
  def __init__(self):
    super().__init__("create", "Create a new container", args_len=1)

  def handle(self, args: list[str]) -> None:
    container = init_container(args[0])
    container.create()


class Delete(Command):
  def __init__(self):
    super().__init__("delete", "Delete a container", args_len=1)

  def handle(self, args: list[str]) -> None:
    container = init_container(args[0])
    container.delete()


class Update(Command):
  def __init__(self):
    super().__init__("update", "Update a container", args_len=1)

  def handle(self, args: list[str]) -> None:
    container = init_container(args[0])
    container.update()


if __name__ == "__main__":
  cli = CLI("box", [Create(), Delete(), Update()])
  cli.handle()
