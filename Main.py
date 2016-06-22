from pprint import pprint
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
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
    # Make sure the table exists
    test = Link.create(
        user="",
        message="",
        time=int(time.time()),
        link=""
    )
    test.delete_instance()
except OperationalError:
    db.create_tables([Link])


def on_chat_message(msg):
    pprint(msg)
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
        text = msg.get("text")
        for url in URLS:
            if url in text:
                # This means the message contains a link to some music, let's save it
                save_link(msg)
                get_fuego(msg)
                break


def save_link(msg):
    entry = Link.create(
            user=msg.get('from').get('username'),
            message=msg.get('text'),
            time=unix_time_to_python_time(msg.get('date')),
            link=get_link(msg)
    )
    entry.save()
# This dictionary keeps track of how fire a track is.
# The key is the message_identifier of the message containing the link, the value is a list
# of the message_identifier of the fuego display and a list of IDs that have sent fuegos.
fuego_count = {}


def get_fuego(msg):
    callback_data = str(telepot.message_identifier(msg))
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='up-fuego \U0001f525', callback_data=callback_data)]
    ])
    bot_msg = bot.sendMessage(msg["chat"]["id"], msg.get('from').get('first_name') +
                    ' with the new hotness!\n', reply_markup=markup)
    fuego_count[callback_data] = [telepot.message_identifier(bot_msg), []]


def on_callback_query(msg):
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    print('Callback query:', query_id, from_id, data)
    add_fuego(query_id, data, from_id)


def add_fuego(query_id, data, from_id):
    try:
        cur_fuego = fuego_count[data]
        if from_id not in cur_fuego[1]:
            cur_fuego[1].append(from_id)
            bot.answerCallbackQuery(query_id, text='fire!')
        else:
            cur_fuego[1].remove(from_id)
            bot.answerCallbackQuery(query_id, text='oops, not fire :(')
        text = ""
        for x in range(len(cur_fuego[1])):
            text += "\U0001f525"
        if text == "":
            text = "Fire?"
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='up-fuego \U0001f525', callback_data=data)]
        ])
        bot.editMessageText(cur_fuego[0], text, reply_markup=markup)
    except KeyError:
        bot.answerCallbackQuery(query_id, text="Can't be voted on anymore!")


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
    # Convert a spotify URI to a spotify URL
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


bot.message_loop({'chat': on_chat_message,
                  'callback_query': on_callback_query})
while 1:
    time.sleep(10)
    # db_debug()
