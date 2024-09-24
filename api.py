from flask import Flask, jsonify, request, send_from_directory, make_response
from models import Player
import requests
import json


app = Flask(__name__)
BALLCHASE_API = 'https://ballchasing.com/api/'

# Read in the data from the JSON files


@app.route('/')
def hello_world():
    return 'Hello, World! This is our Flask backend.'


@app.route('/api/players_average', methods=['GET'])
def get_players_average():
    with open("data.json", "r") as file:
        data = json.load(file)
        players = [Player(*(p.values())) for p in data]
    return jsonify({'player_stats': [player.get_average_stats() for player in players]})


@app.route('/api/get_replay_group/<group_id>', methods=['GET'])
def add_replay_group(group_id: str):
    response = requests.get(BALLCHASE_API + f'groups/{group_id}', 
                            headers={'Authorization': 'API_KEY'})
    
    players = [Player(p['id'], p['name'], 
                    shots=[p['game_average']['core']['shots']], 
                    goals=[p['game_average']['core']['goals']], 
                    assists=[p['game_average']['core']['assists']], 
                    saves=[p['game_average']['core']['saves']], 
                    score=[p['game_average']['core']['score']]) 
                for p in json.loads(response.text)['players']]

    return jsonify({'player_stats': [player.get_average_stats() for player in players]})


@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
