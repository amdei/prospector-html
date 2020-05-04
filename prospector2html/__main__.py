# -*- coding: utf-8 -*-

import sys

from .prospector2html import Prospector2HTML

def main():
    prh = Prospector2HTML()
    sys.exit(prh.main())

if __name__ == '__main__':
    main()