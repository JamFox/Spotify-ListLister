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
        "-c",
        "--cfg",
        default="listlister.conf",
        dest="cfg",
        action="store",
        help="Path to configuration file. Defaults to listlister.conf.",
        type=str,
    )
    optional.add_argument(
        "-o",
        "--out",
        action="store_true",
        help="Output to file instead of terminal if this flag is set.",
    )
    optional.add_argument(
        "-f",
        "--file",
        default=None,
        dest="file",
        action="store",
        help="Path to output file. Defaults to playlists-<USER>.out",
        type=str,
    )
    parser._action_groups.append(optional)
    return parser.parse_args()


async def get_user(client, user_id):
    """Get spotify.User object"""
    return await client.get_user(user_id)


async def get_all_playlists(user):
    """Get list of spotify.Playlist objects"""
    return await user.get_all_playlists()


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
        user = await get_user(client, args.user)
        all_playlists = await get_all_playlists(user)

        if args.out:
            for playlist in all_playlists:
                print(playlist.name)
        else:
            default_output = "playlists-" + args.user + ".out"
            if exists(default_output):
                print(
                    f"A list of this user's playlists was already created. Filename: {default_output}"
                )
            else:
                with open(
                    config.get("output", "output_filename", fallback=default_output),
                    "a",
                ) as f:
                    for playlist in all_playlists:
                        f.write(playlist.name + "\n")


if __name__ == "__main__":
    asyncio.run(main())
