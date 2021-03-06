import json
import os
import pprint

from flask import Flask, request, g
import hipchat
import markdown
app = Flask(__name__)


@app.route('/<room_id>', methods=['GET', 'POST'])
def callback(room_id):
    if request.method == 'HEAD':
        return 'success'

    if not hasattr(g, 'hipchatcli'):
        g.hipchatcli = hipchat.HipChat(os.environ['HIPCHAT_TOKEN'])

    js = json.loads(request.data)
    message, ignore = _get_message(js)

    if not ignore:
        if message is None and 'HIPCHAT_DEBUG_ROOM_ID' in os.environ:
            message = pprint.pformat(js)
            room_id = os.environ['HIPCHAT_DEBUG_ROOM_ID']
        sender = os.environ['HIPCHAT_SENDER']

        if message is not None:
            g.hipchatcli.message_room(room_id, sender, message,
                                      message_format='html')

    return 'success'


def _get_message(js):
    message = None

    # Set ignore to True if there are any actions we want to ignore
    ignore = False

    action = js['action']
    data = action['data']
    if action['type'] == 'updateCard':
        # Move a card from one list to another
        if 'listBefore' in data:
            fmt = ("{action[memberCreator][fullName]} moved {card_link} from "
                   "'{data[listBefore][name]}' to '{data[listAfter][name]}'")
            message = fmt.format(
                action=action, data=data,
                card_link=_card_link(data['board'], data['card']))
        # Rename a card
        elif 'name' in data['old']:
            fmt = ("{action[memberCreator][fullName]} renamed "
                   "'{data[old][name]}' to {card_link}")
            message = fmt.format(
                action=action, data=data,
                card_link=_card_link(data['board'], data['card']))
        # Update card description
        elif 'desc' in data['old']:
            fmt = ("{action[memberCreator][fullName]} updated "
                   "the description for {card_link}")
            message = fmt.format(
                action=action,
                card_link=_card_link(data['board'], data['card']))
        elif 'closed' in data['old']:
            fmt = "{action[memberCreator][fullName]} closed {card_link}"
            message = fmt.format(
                action=action, card_link=_card_link(data['board'], data['card']))
        # Ignore moving a card within a list
        elif 'pos' in data['old']:
            ignore = True
    elif action['type'] == 'updateList':
        # Rename a list
        if 'name' in data['old']:
            fmt = ("{action[memberCreator][fullName]} renamed list "
                   "'{data[old][name]}' to '{data[list][name]}'")
            message = fmt.format(action=action, data=data)
    elif action['type'] == 'commentCard':
        # Comment on a card
        text = markdown.markdown(data['text'])
        fmt = ("{action[memberCreator][fullName]} commented on "
               "{card_link}: {text}")
        message = fmt.format(action=action, data=data, text=text,
                             card_link=_card_link(data['board'], data['card']))
    elif action['type'] == 'createCard':
        # Create a card
        fmt = ("{action[memberCreator][fullName]} added {card_link} "
               "to '{data[list][name]}'")
        message = fmt.format(action=action, data=data,
                             card_link=_card_link(data['board'], data['card']))
    elif action['type'] == 'deleteCard':
        # Delete card
        fmt = ("{action[memberCreator][fullName]} deleted card "
               "'{data[card][idShort]}'")
        message = fmt.format(action=action, data=data)
    elif action['type'] == 'updateCheckItemStateOnCard':
        # Check/Uncheck an item
        if data['checkItem']['state'] == 'complete':
            check = 'checked off'
        else:
            check = 'unchecked'
        fmt = ("{action[memberCreator][fullName]} {check} "
               "'{data[checkItem][name]}' on {card_link}")
        message = fmt.format(
            action=action, check=check, data=data,
            card_link=_card_link(data['board'], data['card']))
    elif action['type'] == 'moveCardToBoard':
        # Move card to the board
        fmt = ("{action[memberCreator][fullName]} moved {card_link} from the "
               "'{data[boardSource][name]}' board to '{data[board][name]}'")
        message = fmt.format(action=action, data=data,
                             card_link=_card_link(data['board'], data['card']))
    elif action['type'] == 'moveCardFromBoard':
        # Move card from the board
        fmt = ("{action[memberCreator][fullName]} moved {card_link} from the "
               "'{data[board][name]}' board to '{data[boardTarget][name]}'")
        message = fmt.format(action=action, data=data,
                             card_link=_card_link(data['board'], data['card']))
    elif action['type'] == 'addMemberToCard':
        # Assign someone to the card
        fmt = ("{action[memberCreator][fullName]} added "
               "{action[member][fullName]} to {card_link}")
        message = fmt.format(action=action,
                             card_link=_card_link(data['board'], data['card']))
    elif action['type'] == 'removeMemberFromCard':
        # Assign someone to the card
        fmt = ("{action[memberCreator][fullName]} removed "
               "{action[member][fullName]} to {card_link}")
        message = fmt.format(action=action,
                             card_link=_card_link(data['board'], data['card']))
    elif action['type'] == 'addMemberToBoard':
        fmt = ("{action[memberCreator][fullName]} added {action[member][fullName]} "
               "to {board_link}")
        message = fmt.format(action=action, board_link=_board_link(data['board']))
    elif action['type'] == 'removeMemberFromBoard':
        fmt = ("{action[memberCreator][fullName]} removed {action[member][fullName]} "
               "to {board_link}")
    elif action['type'] in ['addChecklistToCard', 'removeChecklistFromCard',
                            'createCheckItem', 'deleteComment', 'updateComment']:
        # Ignore all the above types
        ignore = True

    return message, ignore


def _card_link(board, card):
    txt = ("<a href='https://trello.com/card/{board[id]}/{card[idShort]}'>"
           "{card[name]}"
           "</a>").format(
        board=board, card=card)
    return txt

def _board_link(board):
    txt = ("<a href='https://trello.com/board/{board[id]}'>"
           "{board[name]}"
           "</a>").format(board=board)
    return txt

if __name__ == '__main__':
    app.run()
