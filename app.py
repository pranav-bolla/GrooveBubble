from flask import Flask, jsonify, request, json, render_template, redirect, url_for
import spotipy  
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
from pathlib import Path
import urllib
import requests
import os
from dotenv import load_dotenv
load_dotenv()

# Idea for interaction, Show Rank, Name, Top Song
# Use an exponential function for sizing

app = Flask(__name__)

client_id = os.environ.get('client_id')
client_secret = os.environ.get('client_secret')
redirect_uri = os.environ.get('redirect_uri')
scope = os.environ.get('scope')


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/login')
def login():
    return redirect(
        f"https://accounts.spotify.com/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope={'%20'.join(scope.split())}&response_type=code&show_dialog=true"
    )


@app.route("/callback")
def callback():
    auth_code = request.args.get("code")

    token_response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "client_secret": client_secret,
        },
    )
    access_token = token_response.json()["access_token"]
    return redirect(url_for("success", access_token=access_token))


@app.route("/success")
def success():
    access_token = request.args.get("access_token")
    return render_template("index.html", token=access_token)


@app.route('/rjson', methods=['GET'])
def rjson():


    # if (request.method == 'GET'):
    #     f = open('data.json')
    #     data = json.load(f)
    #     return jsonify(data)
    # set up Spotify API client
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='2cae1a89ddd941a3be1ffd58bd3ca544',
                                               client_secret='71770ab297ac4912a1787f923e598eb2',
                                               redirect_uri='http://localhost:5000/callback',
                                               scope='user-top-read'))

    # get user's top artists
    results = sp.current_user_top_artists(limit=50, time_range='long_term')


    filename = "data.json"

    user = {}
    name = sp.current_user()['display_name']
    user[name] = []
    list = []


    for i, item in enumerate(results['items']):
        temp = {}

        items = sp.search(
            q='artist:' + item['name'], type='artist')['artists']['items']

        artist = items[0]
        image_url = artist['images'][0]['url']

        temp["id"] = 50 - i
        temp["artistName"] = item['name']
        temp["imageURL"] = image_url

        user[name].append(temp)

    return user[name]


if __name__ == '__main__':
    app.run(debug=True)
