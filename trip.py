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

    message = None

    # Set ignore to True if there are any actions we want to ignore
    ignore = False

    js = json.loads(request.data)
    action = js['action']
    if action['type'] == 'updateCard':
        data = action['data']
        # Capture moving a card from one list to another
        if 'listBefore' in data:
            fmt = ("{action[memberCreator][fullName]} moved {card_link} from "
                   "'{data[listBefore][name]}' to '{data[listAfter][name]}'")
            message = fmt.format(
                action=action, data=data, 
                card_link=_card_link(data['board'], data['card']))
    elif action['type'] == 'commentCard':
        fmt = ("{action[memberCreator][fullName]} commented on "
               "{card_link}")
        message = fmt.format(action=action, 
                             card_link=_card_link(data['board'], data['card']))
    elif action['type'] == 'createCard':
        fmt = ("{action[memberCreator][fullName]} added {card_link} "
               "to '{data[list][name]}'")
        message = fmt.format(action=action, card_link=_card_link(data['board'],
                             data['card']), data=data)

    if message is None and not ignore:
        message = pprint.pformat(js)

    sender = os.environ['HIPCHAT_SENDER']
    g.hipchatcli.message_room(room_id, sender, message)
    return 'success'


def _card_link(board, card):
    txt = "<a href='https://trello.com/card/{board[id]}/{card[idShort]}'>{card[name]}</a>".format(
        board=board, card=card)
    return txt
    

if __name__ == '__main__':
    app.run()
