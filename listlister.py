#!/usr/bin/env python3

import asyncio
import spotify
import configparser
import argparse
from os.path import exists


def configparse(configfile):
    """Parse config"""
    config = configparser.ConfigParser()
    config.read(configfile)
    return config


def parse_arguments():
    """Parse arguments"""
    parser = argparse.ArgumentParser(
        description="List users playlists and write them to file or terminal."
    )
    optional = parser._action_groups.pop()
    required = parser.add_argument_group("required arguments")
    required.add_argument(
        "-u",
        "--user",
        dest="user",
        action="store",
        help="User ID of whose playlists to list.",
        type=str,
        required=True,
    )
    optional.add_argument(
        "-i",
        "--id",
        action="store_true",
        help="Print playlist IDs instead of names. Works only for file output without tracks flag.",
    )
    optional.add_argument(
        "-t",
        "--tracks",
        action="store_true",
        help="Also list tracks inside the playlists.",
    )
    optional.add_argument(
        "-c",
        "--cfg",
        default="listlister.conf",
        dest="cfg",
        action="store",
        help="Path to configuration file. Defaults to listlister.conf.",
        type=str,
    )
    optional.add_argument(
        "-p",
        "--print",
        action="store_true",
        help="Output to terminal instead of file if this flag is set.",
    )
    optional.add_argument(
        "-o",
        "--out",
        default=None,
        dest="out",
        action="store",
        help="Path to output file. Defaults to playlists-<USER>.out",
        type=str,
    )
    parser._action_groups.append(optional)
    return parser.parse_args()


async def main():
    args = parse_arguments()

    if not exists(args.cfg):
        raise Exception(
            f"ERROR: configuration file at {args.cfg} does not exist.\n Create a configuration file from template listlister.conf.j2 by removing .j2 suffix OR use argument --cfg <path to config> to your custom path instead.\n"
        )
    else:
        config = configparse(args.cfg)

    async with spotify.Client(
        config.get("auth", "id"), config.get("auth", "secret")
    ) as client:
        print(f"Got client connection. Getting info about {args.user}...\n")
        user = await client.get_user(args.user)
        print(f"Got users info. Getting {args.user} playlists...\n")
        all_playlists = await user.get_all_playlists()
        print(f"Everything checks out. Writing list for user {args.user}...\n")

        if args.print:
            for playlist in all_playlists:
                print(playlist.name)
                if args.tracks:
                    tracks = await playlist.get_tracks()
                    for track in tracks:
                        print(track.name + " - " + track.artist.name)
                    print("\n")
        else:
            if args.out:
                output = args.out
            else:
                output = "playlists-" + args.user + ".out"
            if exists(output):
                print(
                    f"A list of this user's playlists was already created, move it or insert a custom output name. Filename: {output}"
                )
            else:
                with open(
                    output,
                    "a",
                ) as f:
                    for playlist in all_playlists:
                        if args.id:
                            f.write(playlist.id + "\n")
                        else:
                            f.write(playlist.name + "\n")
                        if not args.id and args.tracks:
                            tracks = await playlist.get_tracks()
                            for track in tracks:
                                f.write(track.name + " - " + track.artist.name + "\n")
                            f.write("\n")


if __name__ == "__main__":
    asyncio.run(main())
