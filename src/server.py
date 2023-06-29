from fastapi import FastAPI
from pydantic import BaseModel

from context import Context, Container

app = FastAPI(title="Box Runner")

@app.get("/ping")
def ping() -> str:
  return "pong"


class ContainerModel(BaseModel):
  command: str | None = None
  envs: list
  image: str
  name: str
  options: list
  ports: list
  volumes: list


def init_container(body: ContainerModel) -> Container:
  data = body.dict()
  return Context.PrepareContainer(
    name=data.get("name"),
    image_name=data.get("image"),
    command=data.get("command"),
    envs=data.get("envs"),
    volumes=data.get("volumes"),
    ports=data.get("ports"),
    options=data.get("options"),
  )


@app.post("/container", status_code=201)
def create_container(body: ContainerModel) -> None:
  container = init_container(body)
  container.create()


@app.put("/container/{action}")
def update_container(action: str, body: ContainerModel) -> None:
  container = init_container(body)
  if action == "update":
    container.update()
  elif action == "start":
    container.start()
  elif action == "stop":
    container.stop()
  else:
    raise Exception("Invalid action")


@app.delete("/container")
def delete_container(body: ContainerModel) -> None:
  container = init_container(body)
  container.delete()


@app.get("/container/{name}")
def check_container(name: str) -> dict:
  return { "status": Container.Status(name).value }
