
from fabric.api import env, cd, run, task
from fabvenv import virtualenv

import os
import subprocess

import fab_com as fb

env.hosts = fb.config.hosts
env.user = fb.config.user
env.password = fb.config.password

home_dir = fb.config.home_dir
work_dir = os.path.join(home_dir, "google_appengine")
_log = fb._log

@task
def reboot():
    with virtualenv("%s/venv" % home_dir):
        with cd(work_dir):
            run("kill_testresult_server.sh")
            run("start_testresult_server.sh")

@task
def update(is_reboot=False):
    fb.git.commit.local()
    fb.git.commit.remote()
    if is_reboot:
        reboot()


if __name__ == '__main__':

    proc = subprocess.Popen("fab update", cwd='.', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = proc.communicate()
    print "output [{0}], error[{1}]".format(str(out), str(err))
