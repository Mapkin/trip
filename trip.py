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
    js = json.loads(request.data)
    action = js['action']
    message = None
    if action['type'] == 'updateCard':
        data = action['data']
        # Capture moving a card from one list to another
        if 'listBefore' in data:
            fmt = ("{action[memberCreator][fullName]} moved '{data[card][name]}' from "
                   "'{data[listBefore][name]}' to '{data[listAfter][name]}'")
            message = fmt.format(action=action, data=data)

    if message is None:
        message = pprint.pformat(js)
    
    g.hipchatcli.message_room(room_id, sender, message)
    return 'success'


if __name__ == '__main__':
    app.run()
