
import json, sys
from subprocess import Popen, PIPE

# Decorators - just used as a namespace.
def Sublime(origin):
    return origin

def Git(origin):
    return origin

@Sublime
class FolderConfig(object):
    class _FSObject(object):
        def __init__(self):
            self._include = []
            self._exclude = []
        def include(self, items):
            self._include.extend(list(items))
        def exclude(self, items):
            self._exclude.extend(list(items))
    class Folder(_FSObject):
        def __init__(self):
            super(FolderConfig.Folder, self).__init__()
            self._exclude = [".svn", ".git", "out", "Release", "Debug" ]
    class File(_FSObject):
        def __init__(self):
            super(FolderConfig.File, self).__init__()
            self._exclude = ["*.vc", ".sln"]

    def __init__(self, path):
        """ Attribute name used as a key of dict except one starts with '_' """
        self.path = path
        self.name = path

        self._file = FolderConfig.File()
        self.file_include_patterns = self._file._include
        self.file_exclude_patterns = self._file._exclude

        self._folder = FolderConfig.Folder()
        self.folder_include_patterns = self._folder._include
        self.folder_exclude_patterns = self._folder._exclude

    def folder(self):
        return self._folder

    def file(self):
        return self._file

    def dump(self):
        folder = { k:v for k, v in self.__dict__.iteritems()
                   if not k.startswith("_") }
        return folder

@Sublime
class Project(object):

    def __init__(self, name):
        self.config = dict()
        self.config["folders"] = list()
        self.name = name

        self.folderConfig = dict()
        self.file_name = "%s.sublime-project" % self.name

    def add(self, name):
        if name not in self.folderConfig:
            self.folderConfig[name] = FolderConfig(name)
        return self.folderConfig[name]

    def make(self):
        for _, v in self.folderConfig.iteritems():
           self.config["folders"].append(v.dump())

        with open(self.file_name, "w") as project:
            project.write(self.__str__())

    def __str__(self):
        return json.dumps(self.config, sort_keys=True, indent=4)

@Sublime
def makeNaverWebKit():
    sublime = Project("NaverWebKit")
    sublime.add("Source")
    sublime.add("Tools").folder().include(["Tools/shared", "Tools/droid", "Tools/gtk", "Tools/efl", "Tools/jhbuild", "Tools/Scripts", "Tools/WebKitTestRunner", "Tools/TestWebKitAPI", "Tools/MiniBrowser"])
    sublime.make()

@Git
class Config(object):
    def __init__(self):
        cmd = "cmd" if  "windows" in sys.platform else "sh"
        shell  = Popen(cmd, stdin=PIPE, stdout=PIPE, shell=True)
        self.git = shell.stdin
        self.out = shell.stdout

    def set(self, k, v):
        c = "git config --global %s \"%s\"" % (k, v)
        self.git.write(c)

    def done(self):
        self.git.close()
        self.out.close()

@Git
def github():
    git = Config()
    git.set("user.name", "jongdeok.kim")
    git.set("user.email", "devfrog@gmail.com")
    git.done()

@Git
def work():


if __name__ == "__main__":
    #makeNaverWebKit()
