#! /usr/bin/env python3

import json

from yacli import CLI, Command
from container import Container

def open_container(file_path: str) -> Container:
  if not file_path.endswith(".json"):
    raise Exception("Invalid file extesion, try a .json")

  container: Container
  with open(file_path) as file:
    data = json.loads(file.read())
    container = Container.Open(
      name=data.get("name"),
      image_name=data.get("image"),
      envs=data.get("envs"),
      volumes=data.get("volumes"),
      ports=data.get("ports")
    )

  return container


class Create(Command):
  def __init__(self):
    super().__init__("create", "Create a new container", args_len=1)

  def handle(self, args: list[str]) -> None:
    container = open_container(args[0])
    container.create()


class Delete(Command):
  def __init__(self):
    super().__init__("delete", "Delete a container", args_len=1)

  def handle(self, args: list[str]) -> None:
    container = open_container(args[0])
    container.delete()


class Update(Command):
  def __init__(self):
    super().__init__("update", "Update a container", args_len=1)

  def handle(self, args: list[str]) -> None:
    container = open_container(args[0])
    container.update()


if __name__ == "__main__":
  cli = CLI("box", [Create(), Delete(), Update()])
  cli.handle()
