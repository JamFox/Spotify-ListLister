#!/usr/bin/env python3

from random import randint
import argparse
import os
from os.path import exists
import linecache


def parse_arguments():
    """Parse arguments"""
    parser = argparse.ArgumentParser(description="Play a random playlist from a list.")
    parser.add_argument(
        "-pl",
        "--playlists",
        dest="playlists",
        action="store",
        help="List where to pick a playlist from.",
        type=str,
        required=True,
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    file = args.playlists
    if not exists(file):
        print(f"Error: The file {file} does not exist!")
    else:
        with open(file, "r") as f:
            count = sum(1 for _ in f)
            print(f"Number of playlists in file: {count}")
            playnumber = randint(0, count)
        playlist = linecache.getline(file, playnumber)

        print(f"Trying to play playlist number {playnumber}: {playlist}")
        os.system(f"spotify play --playlist {playlist}")


if __name__ == "__main__":
    main()
