#! /usr/bin/env python3

import sys

import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Box Runner")

@app.get("/ping")
def ping() -> str:
  return "pong"


if __name__ == "__main__":
  port = sys.argv[1] if len(sys.argv) > 1 else 8000
  host = sys.argv[2] if len(sys.argv) > 2 else "127.0.0.1"

  uvicorn.run(app, host=host, port=port)
