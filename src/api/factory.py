import os

from api.base import Api
from api.docker import Docker
from api.podman import Podman

API = os.getenv("API") or "podman"

class ProviderFactory:
  @staticmethod
  def Get(name: str = API) -> Api:
    if name == "podman":
      return Podman()
    elif name == "docker":
      return Docker()
    else:
      raise Exception("Invalid provider")
