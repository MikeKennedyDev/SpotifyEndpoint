import os

from azure.appconfiguration import AzureAppConfigurationClient, ConfigurationSetting
from MLibSpotify.SpotifyPlaylist import SpotifyPlaylist
from flask import Flask, render_template, jsonify

app = Flask(__name__)

__playlist_cache = []


@app.route("/songs/<playlist_id>", methods=['GET'])
def get_all_songs(playlist_id):
    print(f'Looking for songs in playlist {playlist_id}')
    playlist = GetPlaylistById(playlist_id)
    return jsonify(playlist.GetAllTracks())


def GetPlaylistById(playlist_id):
    # Using cached playlist
    if playlist_id in [playlist.PlaylistId for playlist in __playlist_cache]:
        print('Playlist found in playlist cache.')
        return next(p for p in __playlist_cache if p.PlaylistId == playlist_id)

    # Creating new playlist model for playlist model
    else:
        print('Playlist not found in cache, retrieving from Spotify.')
        playlist = SpotifyPlaylist(playlist_id=playlist_id,
                                   client_id="bf7bb8ab99894704bed9dfadf4535ef2",
                                   client_secret="44cb0a59f67b4a3dbfdf0ac7c8f4c57a",
                                   refresh_token="AQDwmGYySXf5n3zr-BT9MJhDLJmT4l5pG0dFy2WipLw5AP4dYyp2W4FpOpBltB4XeNFHneApKM9DR3WY5mEwN0aGGXwzgfKA6u-fLGLDjRtLia7gtgnIfQYveZf8yFqkpk8")
        # __playlist_cache.append(playlist)
        return playlist


@app.route("/addTrack/<playlist_id>/<track_id>", methods=['POST'])
def add_song(playlist_id, track_id):
    print(f'Adding {track_id} to {playlist_id}')
    playlist = GetPlaylistById(playlist_id)
    playlist.AddTracks([track_id])
    return f'Added track: {track_id} to playlist: {playlist_id}'


@app.route('/GetTestVar', methods=['GET'])
def testGet():
    print(f'environ: {os.environ}')
    print(f"environ['TestVal']: {os.environ['TestVal']}")
    return "ayy mayb this time"


if __name__ == '__main__':
    app.run()
