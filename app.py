from flask import Flask, render_template, request
import functions

app = Flask(__name__)

token = functions.get_token()
song_info = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/question", methods=["GET", "POST"])
def question():
    if request.method == "POST":
        search = request.form["artist_search"]
        artist = functions.search_for_artist(token, search)
        if artist == None:
            return render_template("error.html", search=search)

        albums = functions.get_albums_by_artist(token, artist['id'])
        if albums == []:
            return render_template("error.html", search=search)

        random_album = functions.get_random_album(albums)
        songs = functions.get_songs_in_album(token, random_album['id'])
        random_song = functions.get_random_song(songs)
        audio = random_song['preview_url']

        song_info.update({
            'song_name': random_song['name'],
            'song_id': random_song['id'],
            'album_name': random_album['name'],
            'album_cover': random_album['images'][0]['url'],
            'album_id': random_album['id'],
            'audio': random_song['preview_url']
        })

        return render_template("question.html", artist=artist['name'], albums=albums,
                               song=random_song['name'], audio=audio)

    if request.method == "GET":
        return "Wrong HTTP method", 400

@app.route("/results", methods=["GET", "POST"])
def results():
    if request.method == "POST":
        album_id = request.form["album"]
        album_name = functions.get_album_info(token, album_id)['name']
        album_cover = functions.get_album_info(token, album_id)['images'][0]['url']
        correct = functions.check_song_in_album(token, album_id, song_info['song_name'])

        return render_template("results.html", guessed_album=album_name, guessed_album_cover=album_cover,
                               song_name=song_info['song_name'], song_album=song_info['album_name'], album_cover=song_info['album_cover'],
                               correct=correct)

    if request.method == "GET":
        return "Wrong HTTP method", 400

if __name__ == '__main__':
    app.run(debug=True)