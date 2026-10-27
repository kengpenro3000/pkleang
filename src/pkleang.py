#!/usr/bin/env python3
# run this script with root privilege


import os
import subprocess
import platform
import shutil
# import time


HOME = os.environ["HOME"]
DISTRO_NAME = platform.freedesktop_os_release()["ID"]
PACKAGE_MANAGERS = {
    # "pkg_manager_name": ["upd_command", "del_commnand"]
    "pacman": ["-Qe", "-R"],


}



def get_pkg_managers(pkg_managers):
    res_managers = {}
    for manager in pkg_managers:
        if shutil.which(manager, path="/usr/bin"):
            res_managers[manager] = pkg_managers[manager]
    return res_managers



def update_pkg_list(managers={"pacman": ["-Qe", "-R"]}): #default distro is arch linux
    # generates a pkg list with defined pkg manager and its command
    pkg_list = []
    # dict = {name : manager}
    pkg_list_managers = {}
    for manager, cmds in managers.items():
        upd_cmd = cmds[0]
        rm_cmd = cmds[1]
        # generates temporary list: ["name1 something1", "name2 something2"]
        pkg_list = list(subprocess.run([manager, upd_cmd], capture_output=True, text=True).stdout.strip().split("\n"))
        print(pkg_list)
        if pkg_list:
            for pkg in pkg_list:
                # split "name1 something1" into ("name1", "something1")
                pkg_name = pkg.split(' ', maxsplit=1)[0]
                pkg_list_managers[pkg_name] = [manager, rm_cmd]
            # if pkg_manager returns nothing - false
        else:
            print(f"{manager} return zero pkgs, check update command")
    return pkg_list_managers


def display_packages(pkg_list , quantity=5): # default word-in-line quantity is 5
    # extracts pkg name from pkg_list dict
    pkg_name_list = list(pkg_list.keys())
    for n in range(len(pkg_name_list)):
        # every {quantity} pkg name is printed at new line
        if n % quantity == 0 and n != 0:
            print()
        print(f"({n+1}){pkg_name_list[n]}", end=' ')
    print()
    print()



def delete_package(manager):
    manager
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
        # check if pkg_index exists in pkg_list
        if 0 <= pkg_index+1 < len(pkg_list):
            return pkg_list[pkg_index]
        else:
            return ''
    else:
        # check if pkg_name exitst in pkg_list
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
    pkg_list = {}
    pkg_managers = get_pkg_managers(PACKAGE_MANAGERS)
    pkg_list = update_pkg_list(pkg_managers)
    #pkg_manager proper output chec
    if pkg_list:
        while True:
            display_packages(pkg_list)
            pkgs_removed = select_pkgs(pkg_list)
            # if user select No or Yes
            if check_choice(pkgs_removed) < 2:
                for pkg_name in pkgs_removed:
                    pkg = {pkg_name: pkg_list[pkg_name]}
                    delete_packages(pkg)
                break
    else:
        print("Oops, something went wrong)")


if __name__ == "__main__":
    # main()
    pkg_managers = get_pkg_managers(PACKAGE_MANAGERS)
    pkg_list = update_pkg_list((pkg_managers))
    print(pkg_list)
