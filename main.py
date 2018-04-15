from pprint import pprint
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import datetime
import time
from peewee import *

# database setup
db = SqliteDatabase('../thegrove/grovedb')

TOKEN = open('TOKEN', 'r').read().strip()
URLS = ["youtube.com/watch", "soundcloud.com/", "open.spotify.com", "spotify:", "youtu.be/", "vimeo.com"]
SPOTIFY_MEDIA_TYPES = ["track", "album", "playlist", "artist", "episode", "show"]
SPOTIFY_BASE_URL = "http://open.spotify.com/"

bot = telepot.Bot(TOKEN)


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
    if not is_new_msg(msg) or not is_text_msg(msg):
        return

    if is_song_url(msg):
        get_fuego(msg)
        save_link(msg)


def is_new_msg(msg):
    cur_time = time.time()
    if cur_time - msg.get("date") < 30:
        return True
    return False


def is_text_msg(msg):
    # content_type is first element of the tuple returned by glance - see docs for more info
    content_type = telepot.glance(msg)[0]
    if content_type != 'text':
        return False
    return True


def is_song_url(msg):
    text = msg.get("text")
    for url in URLS:
        if url in text:
            return True
    return False


# This dictionary keeps track of how fire a track is.
# The key is the message_identifier of the message containing the link, the value is a list
# of the message_identifier of the fuego display and a list of IDs that have sent fuegos.
fuego_count = {}


def get_fuego(msg):
    callback_data = str(telepot.message_identifier(msg))
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='up-fuego \U0001f525', callback_data=callback_data)]
    ])
    user = get_user_identifier(msg)
    bot_msg = bot.sendMessage(msg["chat"]["id"], user +
                              ' with the new hotness!\n', reply_markup=markup)
    fuego_count[callback_data] = [telepot.message_identifier(bot_msg), [], []]


def get_user_identifier(msg):
    # returns either the users first name, username, or a default value in that order of preference
    if msg.get('from').get('first_name'):
        return msg.get('from').get('first_name')
    elif msg.get('from').get('username'):
        return msg.get('from').get('username')
    else:
        return 'nameless goon'


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
        for url in URLS:
            if url in word:
                return word
            elif "spotify:" in word:
                return convert_spotify_uri(text, msg["chat"]["id"])


def convert_spotify_uri(text, chat_id):
    words = text.split()
    pprint(words)
    url = SPOTIFY_BASE_URL[:]
    for word in words:
        if "spotify:" in word:
            if "playlist:" in word:
                url += word.split(":")[-4] + "/" + word.split(":")[-3] + "/" + word.split(":")[-2] + "/" + word.split(":")[-1]
            else:
                url += word.split(":")[-2] + "/" + word.split(":")[-1]
    bot.sendMessage(chat_id, "haha this dumbass doesn't know how to send a spotify link I gotchu bro")
    bot.sendMessage(chat_id, url)
    return url


def on_callback_query(msg):
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    print('Callback query:', query_id, from_id, data)
    add_fuego(query_id, data, from_id, msg)


def add_fuego(query_id, data, from_id, msg):
    try:
        cur_fuego = fuego_count[data]
        upvoted_by = get_user_identifier(msg)
        if from_id not in cur_fuego[1]:
            cur_fuego[1].append(from_id)
            cur_fuego[2].append(upvoted_by)
            bot.answerCallbackQuery(query_id, text='fire!')
        else:
            cur_fuego[1].remove(from_id)
            cur_fuego[2].remove(upvoted_by)
            bot.answerCallbackQuery(query_id, text='oops, not fire :(')
        text = ""
        for x in range(len(cur_fuego[1])):
            text += "\U0001f525 by " + cur_fuego[2][x] + " \n"
        if text == "":
            text = "Fire?"
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='up-fuego \U0001f525', callback_data=data)]
        ])
        bot.editMessageText(cur_fuego[0], text, reply_markup=markup)
    except KeyError:
        bot.answerCallbackQuery(query_id, text="Can't be voted on anymore!")


def unix_time_to_python_time(unix_time):
    return datetime.datetime.fromtimestamp(int(unix_time))


bot.message_loop({'chat': on_chat_message,
                  'callback_query': on_callback_query})
while 1:
    time.sleep(10)


if __name__ == "__main__":
     main()
