import json
import os
import pprint

from flask import Flask, request, g
import hipchat
app = Flask(__name__)

@app.route('/<room_id>', methods=['POST'])
def callback(room_id):
    if not hasattr(g, 'hipchatcli'):
        g.hipchatcli = hipchat.HipChat(os.environ['HIPCHAT_TOKEN'])

    sender = os.environ['HIPCHAT_SENDER']
    data = json.loads(request.data)
    g.hipchatcli.message_room(room_id, sender, pprint.pformat(data))
    return 'success'


if __name__ == '__main__':
    app.run()
