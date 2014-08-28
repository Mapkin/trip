import os

from flask import Flask, g
import hipchat
app = Flask(__name__)

@app.route('/<room_id>', methods='POST')
def callback(room_id):
    if not hasattr(g, 'hipchatcli'):
        g.hipchatcli = hipchat.HipChat(os.environ['HIPCHAT_TOKEN'])

    sender = os.environ['HIPCHAT_SENDER']
    g.hipchatcli.message_room(room_id, sender, 'test')
    return 'success'


if __name__ == '__main__':
    app.run()
