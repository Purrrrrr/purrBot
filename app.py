from flask import Flask, request, jsonify, Response
import requests
from json import dumps, loads
import bot
botApp = Flask(__name__)

server_url = 'http://192.168.230.1:8080' # CHANGE
port = 8774
move_endpoint = '/api/move'
my_address = 'http://192.168.230.67:%d%s' % (port, move_endpoint)

@botApp.route('/api/ping')
def ping(): return "pong\n"

@botApp.route('/api/register/<nick>', methods=['POST'])
def register(nick):
    response = requests.post("%s/register" % server_url,
            json=dict(playerName=nick, url=my_address))
    return jsonify(response.json()['player'])

move_resp = dict((move, Response('"%s"' % move, mimetype='application/json'))
        for move in ('UP', 'DOWN', 'LEFT', 'RIGHT', 'PICK', 'USE'))

@botApp.route(move_endpoint, methods=['POST'])
def move():
    state = request.get_json()
    my_move = bot.move(state)
    return move_resp[my_move]

if __name__ == '__main__': botApp.run(port=port, host="0.0.0.0", debug=True)

