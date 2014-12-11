
import json

def Sublime(original):
    return original

@Sublime
class FolderConfig(object):
    class Folder(object):
        def __init__(self):
            self.include = []
            self.exclude = [".svn", ".git", "out", "Release", "Debug" ]

    class File(object):
        def __init__(self):
            self.include = []
            self.exclude = ["*.vc", ".sln"]

    def __init__(self, path):
        """ Attribute name used as a key of dict except one starts with '_' """
        self.path = path
        self.name = path

        self._file = FolderConfig.File()
        self.file_include_patterns = self._file.include
        self.file_exclude_patterns = self._file.exclude

        self._folder = FolderConfig.Folder()
        self.folder_include_patterns = self._folder.include
        self.folder_exclude_patterns = self._folder.exclude

    def include(self, dest):
        if dest == "folder":
            return self._folder.include
        return self._file.include

    def exclude(self, dest):
        if dest == "folder":
            return self._folder.exclude
        return self._file.exclude

    def dump(self):
        folder = { k:v for k, v in self.__dict__.iteritems()
                   if not k.startswith("_") }
        return folder

@Sublime
class Project(object):

    def __init__(self):
        self.config = dict()
        self.config["folders"] = list()

    def generate(self):
        source = FolderConfig("Source")

        tools = FolderConfig("Tools")
        tools.include("folder").extend(["Tools/shared", "Tools/droid", "Tools/gtk", "Tools/efl", "Tools/jhbuild", "Tools/Scripts", "Tools/WebKitTestRunner", "Tools/TestWebKitAPI", "Tools/MiniBrowser"])

        self.config["folders"].append(source.dump())
        self.config["folders"].append(tools.dump())

    def __str__(self):
        return json.dumps(self.config, sort_keys=True, indent=4)


if __name__ == "__main__":
    sublime = Project()
    sublime.generate()
    print sublime
