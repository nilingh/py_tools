import os
import os.path

# go to "/Users/neil/Documents/eBook/IT资料/Python入门"
wd = os.chdir("/Users/neil/Documents/eBook/IT资料/Python入门")
# get dirname list
dir_list = list(filter(lambda w: os.path.isdir(w), os.listdir(wd)))
# loop rename dirname without space
for old_name in dir_list:
    new_name = old_name.replace(' ', '')
    os.rename(old_name, new_name)


# 简化的版本, 不使用filter
wd = os.chdir("/Users/neil/Documents/eBook/IT资料/Python入门")
for name in os.listdir(wd):
    if os.path.isdir(name):
        os.rename(name, name.replace(' ', ''))
