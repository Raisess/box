import os

from fastapi import FastAPI, Request
from pydantic import BaseModel

from context import Context, Container

API_KEY = os.getenv("API_KEY")

app = FastAPI(title="Box Runner")

@app.middleware("http")
async def before_request(req: Request, next):
  key = req.headers.get("Key")
  if API_KEY:
    if not key or key != API_KEY:
      raise Exception("Invalid key")

  res = await next(req)
  return res


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
  if action == "start":
    container.start()
  elif action == "restart":
    container.restart()
  elif action == "update":
    container.update()
  elif action == "stop":
    container.stop()
  else:
    raise Exception("Invalid action")


@app.delete("/container")
def delete_container(body: ContainerModel) -> None:
  container = init_container(body)
  container.delete()


@app.get("/container/{name}/logs")
def container_status(name: str, since: str = None, until: str = None) -> dict:
  return { "logs": Container.Logs(name, since, until) }


@app.get("/container/{name}/stats")
def container_status(name: str) -> dict:
  return { "stats": Container.Stats(name) }


@app.get("/container/{name}/status")
def container_status(name: str) -> dict:
  return { "status": Container.Status(name).value }


if __name__ == "__main__":
  import sys
  import uvicorn

  port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
  host = sys.argv[2] if len(sys.argv) > 2 else "localhost"

  uvicorn.run(app, host=host, port=port)
