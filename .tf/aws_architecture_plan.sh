#!usr/bin/env bash
# Run this script to all libraries to package them into the lambda function
terraform init

cp -r /c/Users/ASUS/Desktop/spotify/spotienv/Lib/site-packages/requests ../lambda_payloads/avg_album_length_playlist_payload/
cp -r /c/Users/ASUS/Desktop/spotify/spotienv/Lib/site-packages/spotipy ../lambda_payloads/avg_album_length_playlist_payload/

cp /c/Users/ASUS/Desktop/spotify/avg_album_length_playlist.py ../lambda_payloads/avg_album_length_playlist_payload/
cp /c/Users/ASUS/Desktop/spotify/config/playlists.py ../lambda_payloads/avg_album_length_playlist_payload/config/
cp /c/Users/ASUS/Desktop/spotify/tools/playlists.py ../lambda_payloads/avg_album_length_playlist_payload/tools/


cd ../lambda_payloads/avg_album_length_playlist_payload/

zip -r ../../payload.zip '*'

cd ../../.tf/

terraform plan
