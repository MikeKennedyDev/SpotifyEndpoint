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
                                   client_id=os.environ['CLIENT_ID'],
                                   client_secret=os.environ['CLIENT_SECRET'],
                                   refresh_token=os.environ['REFRESH_TOKEN'])
        __playlist_cache.append(playlist)
        return playlist


@app.route("/addTrack/<playlist_id>/<track_id>", methods=['POST'])
def add_song(playlist_id, track_id):
    print(f'Adding {track_id} to {playlist_id}')
    playlist = GetPlaylistById(playlist_id)
    playlist.AddTracks([track_id])
    return f'Added track: {track_id} to playlist: {playlist_id}'


if __name__ == '__main__':
    app.run()
