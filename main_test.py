#!/usr/bin/python3
#-*- encoding: utf8 -*-

import os
import sys

from _8btSpider import _8btSpider
from webManager import app



if __name__ == '__main__':

    # may run in a thread by a day
    _8btpage = _8btSpider.start()

    app.run()
