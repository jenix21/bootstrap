
from fabric.api import env, local, put, cd, get, run, settings
import json

"""
fab.json
{
    "hosts" : [""],
    "user" : "",
    "password" : "",
    "base_dir" : ""
}
"""
f = open("fab.json", "r")
jo = json.load(f)
f.close()

env.hosts = jo["hosts"]
env.user = jo["user"]
env.password = jo["password"]

# remote directory name.
#base_dir = "/development/jdkim/_dev/NaverWebKit_Download/"
base_dir = jo["base_dir"]
bin_dir = base_dir + "WebKitBuild/Release/bin/MiniBrowser/"
script_dir = base_dir + "Tools/Scripts/"

# apk name
apk_name = "DroidWebKit-debug.apk"
pkg_name = "labs.naver.webkit"

# url
url = { "download" : "http://pyvideo.org/video/289/pycon-2010--mastering-python-3-i-o" }


def build():
    with cd(script_dir):
        run("./build-webkit --droid --makeargs=\"--jobs=16\" 2> error.log")

def download():
    with settings(warn_only=True):
        local("rm " + apk_name)
    get(bin_dir + apk_name, apk_name)

def install():
    local("adb uninstall %s" % pkg_name)
    local("adb install " + apk_name)

def load():
    local("adb shell am start -a android.intent.action.VIEW -d %s -n labs.naver.webkit/.MiniBrowser" % url["download"])

def getPid(name):
    ps_lines = local("adb shell ps | grep " + name, capture=True)
    if not ps_lines:
        return "0"
    ps_list = [ ps_line.split()[1] for ps_line in ps_lines.split("\n") ]
    return ps_list, len(ps_list)

def log(mode=None):
    cmd = "adb shell logcat -v time"
    if mode == "dump":
        local(cmd + " -d")
        return
    debug, _ = getPid("debuggerd")
    webkits, _ = getPid(pkg_name)
    grep_cmd = "| grep -e " + debug[0]
    for webkit in webkits:
        grep_cmd += " -e " + webkit

    cmd += grep_cmd
    local(cmd)

def crash():
    cmd = "adb shell logcat -v time -d"
    debug, _ = getPid("debuggerd")
    cmd = cmd + "| grep -e " + debug[0]
    local(cmd)
