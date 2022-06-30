#!/usr/bin/env python3

import re
import sys


def main(file):
    with open(file, mode='rt') as py_file:
        fields = re.findall(r"\s*(\w*)\s*=\s*fields\.", py_file.read())

    print(fields)
    print("\n".join(
        ['<field name="%s"/>' % field for field in fields]
    ))


if __name__ == "__main__":
    print('Hail to you lazy a**es')
    main(sys.argv[1])
