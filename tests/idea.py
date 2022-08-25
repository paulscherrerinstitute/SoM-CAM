#!/usr/bin/env python3
def touch_argv(*argv):
    for arg in argv:
        print(arg)
    # Path(config_file).touch()

def touch(config_file):
    print('echo:', config_file)

def touch_kwargs(**kwargs):
    for key, value in kwargs.items():
        print("%s == %s" % (key, value))
