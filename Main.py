from pprint import pprint
import telepot
import time
import soundcloud
import spotipy

TOKEN = open('TOKEN', 'r').read()
# SCID = open('SOUNDCLOUDID', 'r').read()

# scclient = soundcloud.Client(client_id=SCID)
bot = telepot.Bot(TOKEN)


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



bot.message_loop(handle)

while 1:
    time.sleep(10)