import os
import subprocess

class Shell:
  @staticmethod
  def ExecuteTTY(cmd: str) -> None:
    os.system(cmd)

  @staticmethod
  def Execute(cmd: str) -> str:
    return subprocess.getoutput(cmd)
