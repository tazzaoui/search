#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script decodes and lists the contents of a directory
that contains hex-encoded file names
"""

import base64
import sys
import os

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        exit(1)

    for f in os.listdir(sys.argv[1]):
        print(base64.b16decode(f).decode("latin-1"))
