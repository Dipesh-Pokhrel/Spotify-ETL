import spotipy
import csv
import boto3
import configparser
from datetime import datetime
from spotipy.oauth2 import SpotifyClientCredentials

from config.playlists import spotify_playlist
from tools.playlists import get_artists_from_playlist


config = configparser.ConfigParser()
config.read_file(open('config\spotify.config'))
cid = config.get('Spotify', 'cid')
secret = config.get('Spotify', 'secret')

spotify_object = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=cid , client_secret=secret))

PLAYLIST = "rap_caviar"

def gather_data_local():
    final_data_dictionary = {
        "Year Released": [],
        "Album Length": [],
        "Album Name": [],
        "Artist": [],
    }
    with open('rapcaviar_albums.csv', 'w') as file:
        header = list(final_data_dictionary.keys())
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        albums_obtained = []

        artists = get_artists_from_playlist(spotify_playlist()[PLAYLIST])
        for artist in list(artists.keys()):
            print(artists)
            artist_albums = spotify_object.artist_albums(artist, album_type='album', limit=1)
            for album in artist_albums['items']:
                if "GB" and "US" in album['available_markets']:
                    key = album['name'] + album['artists'][0]['name'] + album['release_date']
                    if key not in albums_obtained:
                        albums_obtained.append(key)
                        album_data = spotify_object.album(album['uri'])
                        # Length of ever album in every song
                        album_length = 0
                        for song in album_data['tracks']['items']:
                            album_length += song['duration_ms']
                        writer.writerow({
                            "Year Released" : album_data['release_date'][:4],
                            "Album Length" : album_length,
                            "Album Name" : album_data['name'],
                            "Artist" : album_data['artists'][0]['name']
                        })
                        final_data_dictionary["Year Released"].append(album_data['release_date'][:4])
                        final_data_dictionary["Album Length"].append(album_length)
                        final_data_dictionary["Album Name"].append(album_data['name'])
                        final_data_dictionary["Artist"].append(album_data['artists'][0]['name'])

    return final_data_dictionary

def  gather_data():
    with open ("/temp/rapcavier_albums.csv", 'w') as file:
        header = ['Year Released', 'Album Length', 'Album Name', 'Artist']
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()

        artists = get_artists_from_playlist(spotify_playlist()[PLAYLIST])
        for artist in artists.keys():
            artists_albums = spotify_object.artist_albums (artist , album_type= 'album', limit=1)
            for album in artists_albums['items']:
                if "GB" in album['items'][0]['available_markets']:
                    album_data = spotify_object.album(album['uri'])
                    album_length = 0 
                    for song in album_data['tracks']['items']:
                        album_length += song['duration_ms']
                    writer.writerow({
                        "Year Released" : album_data['release_date'][:4],
                        "Album Length" : album_length,
                        "Album Name" : album_data['name'],
                        "Artist" : album_data['artists'][0]['name']
                    })
                    

    s3_resource = boto3.resource('s3')
    date = datetime.now()
    filename = f'{date.year}/{date.month}/{date.day}/rapcavier_albums.csv'
    response = s3_resource.Object(Bucket='spotify-playlist-data', Key = filename).upload_file('/temp/rapcavier_albums.csv')
    return response


def lambda_function(event, context):
    gather_data()

if __name__ == '__main__':
   data = gather_data_local()