from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import soundcloud
from requests import HTTPError
from werkzeug.utils import redirect

SCID = open('SOUNDCLOUDID', 'r').read()
client = soundcloud.Client(client_id=SCID)


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app

app = create_app()


@app.route("/pages/<int:page>")
def render_index(page):
    songs = get_songs()
    # we need to get up to 9 entries for whichever page this is, and populate the rows with up to 3 entries each
    first_index = (page - 1) * 9
    last_index = first_index + 9
    total_elements = len(songs)  # TODO: count the rows in the db instead of this
    if last_index > total_elements:
        last_index = total_elements
    cur_songs = songs[first_index:last_index]
    return render_template('index.html', ROW1=render_row(cur_songs[:3]),
                           ROW2=render_row(cur_songs[3:6]), ROW3=render_row(cur_songs[6:]),
                           PAGER=render_pager(page, total_elements))


def render_pager(curpage, total_elements):
    if curpage == 1:
        newer_link = "#"
        newer_disabled = " disabled"
        if total_elements > 9:
            older_disabled = ""
            older_link = "/pages/" + str(curpage + 1)
        else:
            older_disabled = " disabled"
            older_link = "#"
    else:
        newer_link = "/pages/" + str(curpage - 1)
        newer_disabled = ""
        if total_elements > curpage * 9:
            older_disabled = ""
            older_link = "/pages/" + str(curpage + 1)
        else:
            older_disabled = " disabled"
            older_link = "#"
    return render_template("pager.html", DISABLED1=older_disabled, DISABLED2=newer_disabled, OLDER=older_link, NEWER=newer_link)


def render_row(links):
    if len(links) == 0:
        return ""
    # Render a single row of three embeds
    elements = []
    for link in links:
        if "spotify" in link:
            elements.append(render_spotify(link))
        elif "youtu" in link:
            elements.append(render_youtube(link))
        elif "soundcloud" in link:
            elements.append(render_soundcloud(link))
        else:
            pass  # skip any other links
    element1 = elements[0]
    try:
        element2 = elements[1]
    except IndexError:
        element2 = ""
    try:
        element3 = elements[2]
    except IndexError:
        element3 = ""
    return render_template('row.html', ELEMENT1=element1, ELEMENT2=element2, ELEMENT3=element3)


def get_songs():
    # TODO: get songs from db
    links = ["https://open.spotify.com/track/7eRhdHZPcndoK0C9K4rLM5",
    "https://www.youtube.com/watch?v=au0PRVF_RzU",
    "https://soundcloud.com/joshpan/killshot",
    "https://www.youtube.com/watch?v=YMi8pXOaR9M",
    "https://open.spotify.com/track/2djY65hifu2a4R2WqcXqKL",
    "https://soundcloud.com/retrojace/my-boys-ft-yung-lean-prod-by-ducko-mcfli",
    "https://www.youtube.com/watch?v=YBUZNfbJnp4",
    "https://www.youtube.com/watch?v=9vRtx8cICvs",
    "https://www.youtube.com/watch?v=FbO_H4at5Gs",
    "https://soundcloud.com/activexmike/im-a-nobody",
    "https://open.spotify.com/track/6plT7nFGiXKSBP9HFSI4ef",
    "https://soundcloud.com/bip-ling/bip-burger-1"]
    return links


@app.route("/")
def render_home():
    # redirect from the homepage to the first page
    return redirect("/pages/1")


def render_spotify(url):
    # render a spotify embed
    if ':' in url:
        uri = url
    else:
        # Convert this URL to a URI
        url = url.split("/")
        uri = "spotify"
        for x in range(3, len(url)):
            uri += ":" + url[x]
    return render_template('spotify.html', URI=uri)


def render_youtube(url):
    # render a youtube embed
    if "youtu.be" in url:
        uri = url.split("/")[-1]
        if "?" in uri:
            uri = uri.split("?")[0]
    else:
        uri = url.split("=")[-1]

    return render_template("youtube.html", URI=uri)


def render_soundcloud(url):
    # render a soundcloud embed
    if "/sets/" in url:
        print("THIS ISN'T SUPPORTED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")  # TODO: this is gross
    try:
        track = client.get('/resolve', url=url)
    except HTTPError:
        # The soundcloud API will randomly fail on some tracks for no apparent reason
        # see: http://stackoverflow.com/questions/36360202/soundcloud-api-urls-timing-out-and-then-returning-error-403-on-about-50-of-trac
        pass
    return render_template("soundcloud.html", URI=track.id)


if __name__ == "__main__":
    app.run()
