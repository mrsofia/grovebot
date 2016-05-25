from pprint import pprint
import telepot
import time
import soundcloud
import spotipy
import sqlite3
from peewee import *

# database setup
db = SqliteDatabase('grovedb')

TOKEN = 'your-token'
# SCID = open('SOUNDCLOUDID', 'r').read()

# scclient = soundcloud.Client(client_id=SCID)
bot = telepot.Bot(TOKEN)


class Link(Model):
    user = CharField()
    message = TextField()
    # date = DateField()
    time = TimeField()
    link = CharField()

    class Meta:
        database = db

db.connect()
db.drop_tables([Link])
db.create_tables([Link])


def handle(msg):
    pprint(msg)
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        text = str(msg['text'])
        print(text)

        # If some genius sends a spotify URI instead of URL
        if "spotify:track:" in text:
            words = text.split()
            url = "http://open.spotify.com/track/"
            for word in words:
                if "spotify:track:" in word:
                    url += word.split(":")[-1]
            bot.sendMessage(chat_id, "haha this dumbass doesn't know how to send a spotify link I gotchu bro")
            bot.sendMessage(chat_id, url)

            # capture spotify URLs in database
            entry = Link.create(
                user=msg.get('from').get('username'),
                message=msg.get('text'),
                time=msg.get('date'),
                link=url
            )
            entry.save()

        if "youtube.com/watch" in text or "soundcloud.com/" in text or "open.spotify.com" in text:
            entry = Link.create(
                user=msg.get('from').get('username'),
                message=msg.get('text'),
                time=msg.get('date')
            )
            entry.save()


def save_link(msg):
    pass

def get_tracks_by_date(date):
    pass

def convert_spotify_uri(uri):
    pass

bot.message_loop(handle)

while 1:
    time.sleep(10)
