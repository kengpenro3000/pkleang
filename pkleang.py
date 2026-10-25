#!/usr/bin/env python3

import os
import subprocess
import platform
import time

HOME = os.environ["HOME"]
DISTRO_NAME = platform.freedesktop_os_release()["ID"]
PACKAGE_MANAGERS = {
    # "distro_name" : ["pkg_manager_name", "upd_command", "del_commnand"]
    "arch" : ["pacman", "-Qe", "-R"],


}


def update_pkg_list(manager="pacman", cmd="-Qe"): #default distro is arch linux
    # generates a pkg list with defined pkg manager and its command
    pkg_list = list(subprocess.run([manager, cmd], capture_output=True, text=True).stdout.strip().split("\n"))
    if pkg_list:
        # generates dict: {name : version}
        pkg_list = dict(x.split(maxsplit=1) for x in pkg_list)
        return pkg_list
        # if pacman returns nothing - false
    else:
        return False

def display_packages(pkg_list , quantity=5): # default word in line quantity is 5
    # extracts pkg name from pkg_list dict
    pkg_name_list = list(pkg_list.keys())
    for n in range(len(pkg_name_list)):
        if n % quantity == 0 and n != 0:
            print()
        print(pkg_name_list[n], end=' ')
    print()
    print()


def delete_packages(manager, cmd, pkgs):
    subprocess.run([manager, cmd, *pkgs], check=True)

def select_pkgs(pkg_list):
    while True:
        f = 1 # flag that indicates the user has entered all the pkgs correctly
        print("Write pkgs, that you want to delete, separated by a space (e.g \"htop fastfetch\")")
        pkgs_removed = input().split()
        # pkgs validity check
        for pkg in pkgs_removed:
            if pkg not in pkg_list:
                print(f"\"{pkg}\" doen`t exit on your system")
                print()
                f = 0
                break
        #
        if f == 1:
            return pkgs_removed


def main():
    pkg_manager, upd_cmd, del_cmd = PACKAGE_MANAGERS[DISTRO_NAME]
    pkg_list = update_pkg_list(pkg_manager, upd_cmd)
    # pacman proper output check
    if pkg_list:
        display_packages(pkg_list)
        pkgs_removed = select_pkgs(pkg_list)
        print("Are you sure to delete this packages [Y/n]")
        answer = input().lower()
        if not answer or answer == "yes":
            delete_packages(pkg_manager, del_cmd)

    else:
        print("Oops, somthing went wrong)")


if __name__ == "__main__":
    main()
