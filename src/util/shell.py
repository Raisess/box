import os

class Shell:
  @staticmethod
  def Execute(cmd: str) -> None:
    os.system(cmd)
