from shell import Shell

class Image:
  def __init__(self, name: str):
    self.__name = name

  def name(self) -> str:
    return self.__name

  def pull(self) -> None:
    Shell.Execute(f"podman pull {self.__name}")

  def delete(self) -> None:
    Shell.Execute(f"podman image rm {self.__name}")
