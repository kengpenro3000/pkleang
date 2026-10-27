#!/usr/bin/env python3
# run this script with root privilege


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
        return {}

def display_packages(pkg_list , quantity=5): # default word in line quantity is 5
    # extracts pkg name from pkg_list dict
    pkg_name_list = list(pkg_list.keys())
    for n in range(len(pkg_name_list)):
        # every {quantity} pkg name is printed at new line
        if n % quantity == 0 and n != 0:
            print()
        print(f"({n+1}){pkg_name_list[n]}", end=' ')
    print()
    print()


def delete_packages(manager, cmd, pkgs):
    subprocess.run([manager, cmd, *pkgs], check=True)

def select_pkgs(pkg_list):
    pkgs_removed = set()
    pkg_names_list = list(pkg_list.keys())

    while True:
        f = 1 # flag that indicates the user has entered all the pkgs correctly
        print("Write pkgs names or their numbers, separated by a space; you can combine names and numbers (e.g \"htop 1 2 fastfetch\")")
        # pkgs introduced by user
        intorduced_pkgs = input().split()
        # bland list check
        if intorduced_pkgs:
            # pkgs validity check
            for pkg in intorduced_pkgs:
                determened_pkg = determinate_pkg(pkg, pkg_names_list)
                if determened_pkg:
                    pkgs_removed.add(determened_pkg)
                else:
                    print(f"\"{pkg}\" doesn`t exist on your system")
                    print()
                    f = 0
                    break
        else:
            f = 0
        if f == 1:
            return sorted(pkgs_removed)

def determinate_pkg(pkg, pkg_list):
    if pkg.isnumeric():
        # pkg_index-1 because numeration for user starts from 1
        pkg_index = int(pkg)-1
        if 0 < pkg_index+1 < len(pkg_list):
            return pkg_list[pkg_index]
        else:
            return ''
    else:
        if pkg in pkg_list:
            return pkg
        else:
            return ''



def check_choice(pkgs):
    print()
    print(*pkgs)
    print("Are you sure to delete this packages, or want to return to pkg choice? [Y/n/r]")
    answer = input().lower()
    if not answer or answer == 'y':
        return 1
    # variant to users, who want to return to pkg choice
    elif answer == 'r':
        return 2
    else:
        return 0



def main():
    pkg_manager, upd_cmd, del_cmd = PACKAGE_MANAGERS[DISTRO_NAME]
    pkg_list = update_pkg_list(pkg_manager, upd_cmd)
    # pacman proper output check
    if pkg_list:
        while True:
            display_packages(pkg_list)
            pkgs_removed = select_pkgs(pkg_list)
            # if user select No or Yes
            if check_choice(pkgs_removed) < 2:
                delete_packages(pkg_manager, del_cmd, pkgs_removed)
                break
    else:
        print("Oops, something went wrong)")


if __name__ == "__main__":
    main()
