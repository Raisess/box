#! /usr/bin/env python3

import json
import os

from yacli import CLI, Command
from container import Container
from context import Context

def init_context(file_path: str) -> Context:
  if not file_path.endswith(".json"):
    raise Exception("Invalid file extesion, try a .json")
  if not os.path.isfile(file_path):
    raise Exception("Provided file do not exists")

  containers = []
  with open(file_path) as file:
    data = json.loads(file.read())
    if type(data) != list:
      raise Exception("Inalid file format")

    for item in data:
      containers.append(Container.Init(
        name=item.get("name"),
        image_name=item.get("image"),
        envs=item.get("envs") or [],
        volumes=item.get("volumes") or [],
        ports=item.get("ports") or [],
        options=item.get("options") or []
      ))

  return Context(containers)


class Create(Command):
  def __init__(self):
    super().__init__("create", "Create a new container", args_len=1)

  def handle(self, args: list[str]) -> None:
    context = init_context(args[0])
    context.create()


class Delete(Command):
  def __init__(self):
    super().__init__("delete", "Delete a container", args_len=1)

  def handle(self, args: list[str]) -> None:
    context = init_context(args[0])
    context.delete()


class Update(Command):
  def __init__(self):
    super().__init__("update", "Update a container", args_len=1)

  def handle(self, args: list[str]) -> None:
    context = init_context(args[0])
    context.update()


if __name__ == "__main__":
  cli = CLI("box", [Create(), Delete(), Update()])
  cli.handle()
