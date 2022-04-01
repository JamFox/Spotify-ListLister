# Spotify-ListLister

Lists spotify user's playlists.

Discovered a wonderful Spotify account that had over 6k playlists. Only 200 or so of them are displayed when looking at the profile through Spotify's website or app. Needed a way to list a list of all of their playlists so I can listen to the ones I'm interested in.

## Installation

1. Download the source.
2. Create the configuration file:
	- Rename listlister.conf.j2 to listlister.conf and fill in the fields.
	OR 
	- Create your own configuration file and supply the path to it with `-c` or `--cfg`.

Auth configuration is required. Output is optional (that's why it's commented out), defaults to `playlists-<USER>.out`.
```
[auth]
id = <App Client ID>
secret = <App Client Secret>
[output]
#output_filename = <Path and name of file>
```

3. Install dependencies:
	- `pip install spotify`
	OR
	- If you have trouble install packages using requirements.txt in a fresh venv.

## Usage

Run help: 
`python listlister.py -h`

Which displays:
```
listlister.py -h
usage: listlister.py [-h] -u USER [-c CFG] [-o] [-f FILE]

List users playlists and write them to file or terminal.

required arguments:
  -u USER, --user USER  User ID of whose playlists to list.

optional arguments:
  -h, --help            show this help message and exit
  -c CFG, --cfg CFG     Path to configuration file. Defaults to listlister.conf.
  -o, --out             Output to file instead of terminal if this flag is set.
  -f FILE, --file FILE  Path to output file. Defaults to playlists-<USER>.out
```