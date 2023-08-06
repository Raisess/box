import os
import subprocess

class Shell:
  @staticmethod
  def ExecuteTTY(cmd: str) -> None:
    exit_code = os.system(cmd)

  @staticmethod
  def Execute(cmd: str) -> str:
    [exit_code, output] = subprocess.getstatusoutput(cmd)
    if exit_code != 0:
      raise Exception(f"Command failed to execute: {cmd}")

    return output
