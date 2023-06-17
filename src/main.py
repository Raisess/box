#! /usr/bin/env python3

import json
import os

from yacli import CLI, Command
from context import Context

def init_context(file_path: str) -> Context:
  if not os.path.isfile(file_path):
    raise Exception("Provided file do not exists")
  if not file_path.endswith(".json"):
    raise Exception("Invalid file extesion, try a .json")

  containers = []
  with open(file_path) as file:
    data = json.loads(file.read())
    if type(data) != list:
      raise Exception("Inalid file format")

    for item in data:
      containers.append(Context.PrepareContainer(
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
    super().__init__("create", "Create new containers", args_len=1)

  def handle(self, args: list[str]) -> None:
    context = init_context(args[0])
    context.create()


class Start(Command):
  def __init__(self):
    super().__init__("start", "Start containers", args_len=1)

  def handle(self, args: list[str]) -> None:
    context = init_context(args[0])
    context.start()


class Stop(Command):
  def __init__(self):
    super().__init__("stop", "Stop containers", args_len=1)

  def handle(self, args: list[str]) -> None:
    context = init_context(args[0])
    context.stop()


class Update(Command):
  def __init__(self):
    super().__init__("update", "Update containers", args_len=1)

  def handle(self, args: list[str]) -> None:
    context = init_context(args[0])
    context.update()


class Delete(Command):
  def __init__(self):
    super().__init__("delete", "Delete containers", args_len=1)

  def handle(self, args: list[str]) -> None:
    context = init_context(args[0])
    context.delete()


if __name__ == "__main__":
  cli = CLI("box", [Create(), Start(), Stop(), Delete(), Update()])
  cli.handle()
