import click
import hipchat
import trello


def callback_url(domain, room_id, model_id):
    # Ignore model_id
    return 'http://{domain}/{room_id}'.format(domain=domain, room_id=room_id)


@click.group()
@click.option('--trello-app-key', envvar='TRELLO_APP_KEY')
@click.option('--trello-token', envvar='TRELLO_USER_TOKEN')
@click.option('--hipchat-token', envvar='HIPCHAT_TOKEN')
@click.pass_context
def trip(ctx, trello_app_key, trello_token, hipchat_token):
    trellocli = trello.TrelloClient(api_key=trello_app_key, token=trello_token)
    hipchatcli = hipchat.HipChat(token=hipchat_token)
    ctx.obj = (trellocli, hipchatcli)


# Define boards group
@trip.group()
def boards():
    pass


@boards.command(name='list')
@click.pass_context
def listboards(ctx):
    trellocli = ctx.obj[0]
    boards = trellocli.list_boards()
    for board in boards:
        print('{0.name}: {0.id}'.format(board))


# Define webhooks group
@trip.group()
def webhooks():
    pass


@webhooks.command(name='list')
@click.pass_context
def listwebhooks(ctx):
    trellocli = ctx.obj[0]
    hooks = trellocli.list_hooks()
    for hook in hooks:
        print('{0.callback_url}: {0.id}'.format(hook))


@webhooks.command(name='create')
@click.option('--domain')
@click.option('--room-id')
@click.argument('model-id')
@click.pass_context
def createwebhook(ctx, domain, room_id, model_id):
    trellocli = ctx.obj[0]
    url = callback_url(domain, room_id, model_id)
    trellocli.create_hook(url, model_id)


@webhooks.command(name='remove')
@click.argument('hook-id')
@click.pass_context
def removewebhook(ctx, hook_id):
    trellocli = ctx.obj[0]
    trello.WebHook(trellocli, None, hook_id=hook_id).delete()


# Define hipchat rooms group
@trip.group()
def rooms():
    pass


@rooms.command(name='list')
@click.pass_context
def listrooms(ctx):
    hipchatcli = ctx.obj[1]
    rooms = hipchatcli.list_rooms()
    for room in rooms['rooms']:
        print("{0[name]}: {0[room_id]}".format(room))


@rooms.command(name='message')
@click.option('--roomid')
@click.option('--sender', default='trip')
@click.argument('message')
@click.pass_context
def messageroom(ctx, roomid, sender, message):
    hipchatcli = ctx.obj[1]


if __name__ == '__main__':
    trip()
