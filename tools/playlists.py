import spotipy

import configparser
config = configparser.ConfigParser()
config.read_file(open('config\spotify.config'))
cid = config.get('Spotify', 'cid')
secret = config.get('Spotify', 'secret')

spotify = spotipy.Spotify(client_credentials_manager=spotipy.oauth2.SpotifyClientCredentials(client_id=cid , client_secret=secret))

def get_artists_from_playlist(playlist_uri):
    playlist_tracks = spotify.playlist_tracks(playlist_id=playlist_uri)
    artists = []
    for song in playlist_tracks['items']:
        if song['track']:
            print(song['track']['artists'][0]['name'])
            artists[song['track']['artists'][0]['uri']] = song['track']['artists'][0]['name']
    return artists

