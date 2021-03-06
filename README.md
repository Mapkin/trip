Trip
====
Post Trello activity to Hipchat

Usage
-----
Configuration is done via the command line.

Set the following environment variables, they can be set on the command
line using the corresponding options

* `HIPCHAT_TOKEN` `--hipchat-token`: API token from Hipchat
  activity
* `TRELLO_APP_KEY` `--trello-app-key`: Trello Key
* `TRELLO_USER_TOKEN` `--trello-token`: Trello auth token
* `TRELLO_SECRET_KEY`: (unused)
* `HIPCHAT_DEBUG_ROOM_ID`: Optional Hipchat room ID for unreconized Trello
* `HIPCHAT_SENDER`: The name of the Hipchat user to post

Note that `HIPCHAT_DEBUG_ROOM_ID` and `HIPCHAT_SENDER` are not needed for the
command line application

Here are commands to run:

* `tripcli.py boards list` - List Trello boards and their Trello ModelID
* `tripcli.py rooms list` - List available Hipchat rooms and their Hipchat
RoomID
* `tripcli.py webhooks list` - List the Trello webhooks and ID currently running
* `tripcli.py webhooks create --domain DOMAIN --room-id ROOMID MODEL_ID` to
  create a new webhook.
* `tripclip.py webhooks remove WEBHOOKID` - Remove a Trello webhook

Note that when you create a webhook, Trello tries to hit the server so it must
be up and running otherwise it will fail.

A typical use might look like:

`$ tripcli.py boards list` - copy the Trello board you want to follow

`$ tripcli.py rooms list` - copy the Hipchat room you want to follow

`$ tripcli.py webhooks create --domain tripbot.domain.com --room-id ROOMID MODELID`

Keys
----
Log in to Trello and visit https://trello.com/1/appKey/generate. Grab the key
and set the environment variable (or use it appropriately on the command
line).
To get the user token you need to go through the auth flow. See here:
https://trello.com/docs/gettingstarted/#getting-a-token-from-a-user

Hipchat needs an admin token - generated from the "API" tab on the Hipchat
website after logging in.
