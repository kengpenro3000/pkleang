from copy import copy

frequently_words = {"lib": []}
skip_list = ["libreoffce", "libresprite", "librewolf"]

c = 0
for f in open("pkg-list.txt", "r"):
    c += 1
    pkg_name, pkg_version = f.strip().split()
    pkg_name_words = copy(pkg_name).split('-')
    # input(pkg_name)

    if pkg_name in skip_list:
        continue

    if len(pkg_name) >= 3 and "lib" in pkg_name:
        frequently_words["lib"].append(pkg_name)

    else:
        # f = 0
        keys = frequently_words.keys()
        for word in pkg_name_words:
            if word in keys:
                frequently_words.setdefault(word, [pkg_name])
                frequently_words[word].append(pkg_name)

print(c)

while True:
    print("Do you want to list pkgs with frequently words? [y/N] ", end='')
    answer = input().strip().lower()
    if answer == '' or answer == 'n':
        break
    elif answer == 'y':
        for word, items in frequently_words.items():
                # if len(items) > 8:
                print(f"{word} :")
                for item in items:
                    print(item)
                print(f"{word.capitalize()} pkgs count: {len(items)}")
        break
