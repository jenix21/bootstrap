# -*- coding: utf-8 -*-

from fabric.api import env, local, put, cd, run

import json
import fnmatch
import os
import sys

class Config():
    """
    keys in json file (hosts,user,password,home_dir,work_dir)
    """
    _file_name = "fab_config.json"
    def __init__(self):
        jsn = None
        try:
            f = open(self._file_name, "r")
            jsn = json.load(f)
            f.close()
        except Exception as e:
            print sys.stderr, "Error occured loading config (%s)", str(e)
        else:
            for k in jsn.keys():
                setattr(self, k, jsn[k])

class Git():
    """
    git.commit.local()
    git.commit.remote()
    """
    class commit():
        pass
    def __init__(self, work_dir="", branch="master"):
        Git.commit.local = self._commit_local
        Git.commit.remote = self._commit_remote
        self._branch = branch
        self._work_dir = work_dir
    def _gen_log_msg(self):
        files = local("git diff --cached --name-only", capture=True).split(os.linesep)
        if len(files):
            return "%d files changed including %s" % (len(files), files[0])
    def _commit_local(self):
        env.warn_only = True
        with cd(""):
            local("git add -u")
            local("git commit -m \"%s\"" % self._gen_log_msg())
            local("git push origin %s" % self._branch)
        env.warn_only = False
    def _commit_remote(self):
        with cd(self._work_dir):
            run("git pull origin %s" % self._branch)

config = Config()
git = Git(work_dir=config.work_dir)

def _log(msg):
    print " * %s" % msg.replace("_", " ")

def upload_files():
    """
    Not used, left as a code snippet.
    :return:
    """
    commited_files = local("git show --pretty='format:' --name-only", capture=True).split(os.linesep)
    files_to_upload = filter(lambda f: "master" in f or "slave" in f, commited_files)

    for file in files_to_upload:
        put(file, "%s/%s" % (config.work_dir, file))

def delete_pyc():
    _log(__name__)
    for root, dirnames, filenames in os.walk("."):
        for filename in fnmatch.filter(filenames, "*.pyc"):
            os.remove(filename)

