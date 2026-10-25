#/usr/bin/python3

import os
import subprocess
import platform

HOME = os.environ["HOME"]
DISTRO_NAME = platform.freedesktop_os_release()["ID"]
PACKAGE_MANAGERS = {
    # "distro_name" : ["pkg_manager_name", "upd_command", "..."]
    "arch" : ["pacman", "-Qe"],


}

pkg_list = list()
pkg_manager, upd_cmd = PACKAGE_MANAGERS[DISTRO_NAME]

print(DISTRO_NAME, HOME)
def update_pkg_list(): #default distro is arch linux
        pkg_list = list(subprocess.run([pkg_manager, upd_cmd], capture_output=True, text=True).stdout.strip().split("\n"))
        print(pkg_list)

# def pkg_list_processor():
    # with open("pkg-list.txt") as f:
        # pkg_list =

if __name__ == "__main__":
    update_pkg_list()
