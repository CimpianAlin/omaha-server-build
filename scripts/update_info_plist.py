#!/usr/bin/env python

import argparse
import plistlib

def main(path, to_add):
    plist = plistlib.readPlist(path)

    for i in to_add:
        i = i.split('=')
        print("[INFO] Setting {} to {}".format(i[0], i[1]))
        plist[i[0]] = i[1]

    plistlib.writePlist(plist, path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update Info.plist for omaha-server testing")
    parser.add_argument('--set', required=False, action='append', help="[Key=Value] Sets plist Key to Value, can be specified multiple times")
    parser.add_argument('path', help="Path Info.plist to update")

    args = parser.parse_args()

    main(args.path, args.set)