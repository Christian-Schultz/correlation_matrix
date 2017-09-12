import sys
import os

SRC_PATH = os.path.realpath('../src/')

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)