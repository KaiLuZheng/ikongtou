#!/usr/bin/python3
#-*- encoding: utf8 -*-

import os
import sys


main_dir = (os.path.dirname(os.path.realpath(__file__)))
ispider_dir = main_dir + '/ispider'
sys.path.append(ispider_dir)


from webManager import app


if __name__ == '__main__':
    app.run()
