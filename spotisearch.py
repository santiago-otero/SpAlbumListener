import os
from requests import post, get
from flask import Flask, request, redirect, session, url_for, render_template
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
import requests

app = Flask(__name__)
app.secret_key = os.urandom(64)

# get your passwords form a .env file for safer use. Remember to use dotenv module
client_id = os.environ.get('SP_ClIENT_ID')
client_secret = os.environ.get('SP_CLIENT_SECRET')
redirect_uri = 'http://localhost:5000/callback'

cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    cache_handler=cache_handler,
    show_dialog=True
)

# whenever we want data from the spotify api we need to call sp. spotify method 
sp = Spotify(auth_manager=sp_oauth)

@app.route('/')
def home():
    # check if token is valid, if not do the login again
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for('spotisearch'))


@app.route('/about')
def about():
    return render_template('about.html')

    
@app.route('/callback')
def callback():
    # handle users cancelation to log-in to reprompt again 
    if 'code' in request.args:
        token_info = sp_oauth.get_access_token(request.args['code'])
        session['AUTH_TOKEN'] = token_info['access_token']
        return redirect(url_for('spotisearch'))
    else:
        # Handle case where 'code' parameter is not present in the request to redirect default home page
        return redirect(url_for('home'))

def get_artist_json(artist):
    # handle token expirancy
    if 'AUTH_TOKEN' in session:
        try:
            if not sp_oauth.validate_token(cache_handler.get_cached_token()):
                auth_url = sp_oauth.get_authorize_url()
                return redirect('/')
                
            url = "https://api.spotify.com/v1/search?"
            access_token = session['AUTH_TOKEN']
            headers = {"Authorization": f"Bearer {access_token}"}  
            query = f"q={artist}&type=artist"

            query_url = url + query
            result = get(query_url, headers=headers)
            json_result = result.json()
            json_object_artists = json_result['artists']
            json_object_items =  json_object_artists['items']
            json_object_follows = json_object_items[0]
            return json_object_follows
        except IndexError:
            return None
    else:
        return None

def get_artist_id(artist_json):
    if artist_json:
        return artist_json.get('id')
    else:
        return None

def get_artist_albums(artist_id):
    try:
        access_token = session.get('AUTH_TOKEN')
        if access_token:
            url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
            headers = {"Authorization": f"Bearer {access_token}"}
            params = {
                'include_groups': 'album',
                'market': 'ES',
                'limit': 5,
                'offset': 0,
            }

            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Raise an error for bad status codes

            albums_response = response.json()
            # Iterate through every album uri and append it to an empty list:
            album_uris = [item["uri"] for item in albums_response.get("items", [])]
            return album_uris
        else:
            # Handle case where AUTH_TOKEN is not available in session
            return None
    except requests.RequestException as e:
        print("Error fetching albums:", e)
        return None


# Initialize artist_id as None here, inside the conditional block
artist_id = None

# initialize artist name that user inputs
artist_json_name = None

@app.route('/spotisearch', methods=['GET', 'POST'])
def spotisearch():
    if 'AUTH_TOKEN' in session:
        access_token = session['AUTH_TOKEN']
    
        global artist_id

        if request.method == 'POST':
            artist_json_name = str(request.form['artist_name']).strip().capitalize()
            artist_json = get_artist_json(artist_json_name)

             # handle if artist_data is none
            if artist_json is not None:

                # Update artist_id with the result of get_artist_id
                artist_id = get_artist_id(artist_json)

                albums_json_response = get_artist_albums(artist_id)

                # Initialize the album variables with None
                album1 = album2 = album3 = album4 = album5 = None

                # Check if albums_json_response exist
                if albums_json_response:
                    try:
                        # try assigning each album to it´s position in case it exist
                        album_uris = []
                        for uri in albums_json_response:
                            album_uris.append(uri)

                    except IndexError:
                        album_uris = []

                    # in case the artist has no albums or does not exist: 
                    initial_uri = album_uris[0] if album_uris else None

                    return render_template('main.html', data=artist_json, 
                                    albums_json_response=albums_json_response,
                                    initial_uri=initial_uri, album_uris=album_uris)
                else:
                    return render_template('main.html', data=artist_json)
            else:
                error = "artist does not exist"
                return render_template('main.html', data= artist_json, error=error)
        
        return render_template('main.html', data=None)
    return render_template('main.html', data=None)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('home'))
    else:
        # Handle GET request, maybe redirect somewhere else or render a different page
        return redirect(url_for('home'))
if __name__ == '__main__':
    app.run(debug=False)
