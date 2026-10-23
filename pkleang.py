import os

HOME = os.environ["HOME"]
# print(os.stat("/"))
# print(os.name)
# print(os.getcwd())
# os.system(f"cat {HOME}/pkleang/pkleang.py")
# print(HOME)
answer = input("Do you want to update the system? [y/N]")
if answer.lower() == "y":
    os.system("sudo pacman -Suy")
