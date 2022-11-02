from MLibSpotify.SpotifyPlaylist import SpotifyPlaylist, AuthorizationValues
from flask import Flask, render_template, jsonify

app = Flask(__name__)

scope = 'playlist-read-collaborative playlist-modify-public'
__authorization = AuthorizationValues(client_id='bf7bb8ab99894704bed9dfadf4535ef2',
                                      client_secret='44cb0a59f67b4a3dbfdf0ac7c8f4c57a',
                                      scope=scope,
                                      redirect_uri='https://example.com/callback/')

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
        playlist = SpotifyPlaylist(authorization_values=__authorization, playlist_id=playlist_id)
        __playlist_cache.append(playlist)
        return playlist


@app.route('/testioli')
def test():
    print('In Testioli')
    return jsonify("Hello testioli")


@app.route('/spotifyTest')
def spotifyTest():
    print('Creating playlist')
    playlist = SpotifyPlaylist(authorization_values=__authorization, playlist_id='2UmDYQxgIDaKikeG53Ffd5')
    print('Playlist created')
    return jsonify("Get this")


@app.route('/getScope')
def getScope():
    return jsonify(scope)


@app.route('/getAuth')
def getAuth():
    print(__authorization)
    print(str(__authorization))
    return jsonify(str(__authorization))


if __name__ == '__main__':
    app.run()
