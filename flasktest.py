from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import soundcloud

SCID = open('SOUNDCLOUDID', 'r').read()
client = soundcloud.Client(client_id=SCID)


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app

app = create_app()
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
         "https://open.spotify.com/track/6plT7nFGiXKSBP9HFSI4ef"]


@app.route("/")
def hello():
    return render_template('index.html', ROW1=render_row(links))


def render_spotify(url):
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
    if "youtu.be" in url:
        uri = url.split("/")[-1]
        if "?" in uri:
            uri = uri.split("?")[0]
    else:
        uri = url.split("=")[-1]

    return render_template("youtube.html", URI=uri)


def render_soundcloud(url):
    if "/sets/" in url:
        print("THIS ISN'T SUPPORTED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    track = client.get('/resolve', url=url)
    return render_template("soundcloud.html", URI=track.id)


def render_row(links):
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
    return render_template('row.html', ELEMENT1=elements[0], ELEMENT2=elements[1], ELEMENT3=elements[2])


if __name__ == "__main__":
    app.run()
