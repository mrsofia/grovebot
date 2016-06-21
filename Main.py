from pprint import pprint
import telepot
import datetime, time
# import soundcloud
# import spotipy
from peewee import *

# database setup
db = SqliteDatabase('grovedb')

TOKEN = open('TOKEN', 'r').read()
# SCID = open('SOUNDCLOUDID', 'r').read()

# scclient = soundcloud.Client(client_id=SCID)
bot = telepot.Bot(TOKEN)

URLS = ["youtube.com/watch", "soundcloud.com/", "open.spotify.com", "spotify:track:"]


class Link(Model):
    user = CharField()
    message = TextField()
    time = DateTimeField()
    link = TextField()

    class Meta:
        database = db

db.connect()
try:
    test = Link.create(
        user="",
        message="",
        time=int(time.time()),
        link=""
    )
    test.delete_instance()
except OperationalError:
    db.create_tables([Link])


def handle(msg):
    pprint(msg)
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
        text = msg.get("text")

        for url in URLS:
            if url in text:
                save_link(msg)
                break


def save_link(msg):
    entry = Link.create(
            user=msg.get('from').get('username'),
            message=msg.get('text'),
            time=unix_time_to_python_time(msg.get('date')),
            link=get_link(msg)
    )
    entry.save()


def get_link(msg):
    # Get the link out of the message
    text = msg.get('text')
    words = text.split()
    for word in words:
        for url in URLS[:-1]:
            if url in word:
                return word
            elif "spotify:track:" in word:
                return convert_spotify_uri(text, msg["chat"]["id"])


def get_tracks_by_date(date):
    pass


def convert_spotify_uri(text, chat_id):
    words = text.split()
    url = "http://open.spotify.com/track/"
    for word in words:
        if "spotify:track:" in word:
            url += word.split(":")[-1]
    bot.sendMessage(chat_id, "haha this dumbass doesn't know how to send a spotify link I gotchu bro")
    bot.sendMessage(chat_id, url)
    return url


def unix_time_to_python_time(unix_time):
    return datetime.datetime.fromtimestamp(int(unix_time))


def db_debug():
    # Prints everything in the database
    print("CURRENT DATABASE STATE")
    for link in Link.select():
        print(link.user, "|", link.message, "|", link.time, "|", link.link)

bot.message_loop(handle)
while 1:
    time.sleep(10)
    #db_debug()
