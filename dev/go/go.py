import argparse
import os
from subprocess import call
import sys

def _error(msg, exit=False):
  sys.stderr.write(msg + os.linesep)
  sys.exit(1) if exit else None

class GoScaffold(object):
  DIRS = ["bin", "pkg", "src"]
  def __init__(self):
    self.is_scaffolded = all(map(lambda d : os.path.exists(d), self.DIRS))
  def is_in_project(self):
    return self.is_scaffolded
  def make(self, name):
    if not os.path.exists(name):
      os.mkdir(name)
    for dir in self.DIRS:
      os.mkdir(os.path.join(name, dir))


def main():
  GO_CMD = ["build", "clean", "doc", "env", "fix", "fmt", "generate", "get", "install", "list", "run", "test", "tool", "version", "vet"]

  parser = argparse.ArgumentParser()
  parser.add_argument("cmd", help="go command or extended cmd")
  parser.add_argument("cmd_opt", nargs="*", help="go command option")
  args = parser.parse_args()

  scaffold = GoScaffold()

  command = args.cmd
  options = args.cmd_opt

  if command in GO_CMD and scaffold.is_in_project():
    _error("check if you have bin, pkg, src directories.", True)

  if "make" in command and options:
    scaffold.make(options[0])
    return

  call("go.exe {}, {}".format(command, " ".join(options)).split())

if __name__ == "__main__":
  main()