from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from MLibSpotify.SpotifyPlaylist import SpotifyPlaylist, AuthorizationValues

app = Flask(__name__)

scope = 'playlist-read-collaborative playlist-modify-public'
__authorization = AuthorizationValues(client_id='bf7bb8ab99894704bed9dfadf4535ef2',
                                      client_secret='44cb0a59f67b4a3dbfdf0ac7c8f4c57a',
                                      scope=scope)

__playlist_cache = []


@app.route('/')
def index():
    print('Request for index page received')
    return render_template('index.html')


@app.get("/songs/<playlist_id>")
def get_all_songs(playlist_id):
    playlist = GetPlaylistById(playlist_id)
    return jsonify(playlist.GetAllTracks())


def GetPlaylistById(playlist_id):
    # Using cached playlist
    if playlist_id in [playlist.PlaylistId for playlist in __playlist_cache]:
        return next(p for p in __playlist_cache if p.PlaylistId == playlist_id)

    # Creating new playlist model for playlist model
    else:
        playlist = SpotifyPlaylist(authorization_values=__authorization, playlist_id=playlist_id)
        __playlist_cache.append(playlist)
        return playlist


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/hello', methods=['POST'])
def hello():
    name = request.form.get('name')

    if name:
        print('Request for hello page received with name=%s' % name)
        return render_template('hello.html', name=name)
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return redirect(url_for('index'))


@app.route('/testioli')
def test():
    return jsonify("Hello testioli")


@app.get('/gettest')
def gettest():
    return jsonify("Get this")


if __name__ == '__main__':
    app.run()
