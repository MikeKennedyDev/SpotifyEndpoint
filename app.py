import os

from MLibSpotify.SpotifyPlaylist import SpotifyPlaylist
from flask import Flask, render_template, jsonify

app = Flask(__name__)

__playlist_cache = []


@app.get("/songs/<playlist_id>")
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
                                   access_token="BQAvGVCxcM1mDPuoO0dVnFby1j8cKkLPME8ieerhGNMVKqVjPhCsGNMmAlu21xMczLj92QBjZI7GC-YeAKHFE4RqM68QgCrtpF_jl1JsvY8qhpQvw-zbDjnu-NnxhtcKRE_67EwsjeZHdTCAP4gbQf76MmKa5HV_KqqqbKb6NN5WC85u97Y2crWZOfqzKqZfxVaHQmiV01o1ftFaSDs")
        __playlist_cache.append(playlist)
        return playlist


@app.post("/addTrack/<playlist_id>/<track_id>")
def add_song(playlist_id, track_id):
    print(f'Adding {track_id} to {playlist_id}')
    playlist = GetPlaylistById(playlist_id)
    playlist.AddTracks([track_id])
    return f'Added track: {track_id} to playlist: {playlist_id}'


if __name__ == '__main__':
    app.run()
