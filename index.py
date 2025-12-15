import base64
import requests
from dotenv import load_dotenv
import os
import json

load_dotenv('.env')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# creating a token for spotify
def access_token():
        try:
                credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
                encoded_credentials = base64.b64encode(credentials.encode()).decode()
                response = requests.post(
                        'https://accounts.spotify.com/api/token',
                        headers={"Authorization": f'Basic {encoded_credentials}'},
                        data={'grant_type': 'client_credentials'}
                )
                response.raise_for_status()
                token = response.json().get('access_token')
                if not token:
                        raise Exception('no access token in response')
                print("token generated successfully...")
                return token
        except Exception as e:
                print("error in token generation..", e)
                return None

# print(access_token())



# latest release in spotify
def get_new_release():
        try:
                token = access_token()
                if not token:
                        print('No token available; aborting.')
                        return
                header = {'Authorization': f'Bearer {token}'}
                params = {'limit': 50}
                response = requests.get(
                        'https://api.spotify.com/v1/browse/new-releases',
                        headers=header,
                        params=params
                )

                if response.status_code == 200:
                        data = response.json()
                        releases = []
                        albums = data.get('albums', {}).get('items', [])
                        for album in albums:
                                info = {
                                        'album_name': album.get('name'),
                                        'artist_name': album.get('artists', [{}])[0].get('name'),
                                        'release_date': album.get('release_date'),
                                        'album_type': album.get('album_type'),
                                        'total_tracks': album.get('total_tracks'),
                                        'spotify_url': album.get('external_urls', {}).get('spotify'),
                                        'album_image': album.get('images', [None])[0].get('url') if album.get('images') else None
                                }
                                releases.append(info)
                                print(json.dumps(info, indent=2))
                        return releases
                else:
                        print('Failed to fetch new releases:', response.status_code, response.text)
        except Exception as e:
                print("Error in latest release data fetching...", e)

if __name__ == '__main__':
        get_new_release()



        

    
