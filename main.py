from flask import Flask, render_template
from dynamo_db import dynamo_db
from s3_manager import s3_manager
import json

app = Flask(__name__)
db = dynamo_db()

def create_s3_bucket(name, region=None):
    client = s3_manager()
    client.create_bucket(name)


def upload_artist_images():
    client = s3_manager()
    bucket_name = 's3500659-artist-images'

    with open('a2.json') as json_data:
            data = json.load(json_data)
            for item in data['songs']:
                artist = json.dumps(item['artist']).strip('"')
                image_url = json.dumps(item['img_url']).strip('"')

                client.upload_image_url_to_bucket(bucket_name, artist + ".jpg", 
                        image_url)
                

def initialise_music_table():
    # create the music
    if db.table_exist('music') == False:
        db.create_music_table()
        # load music data
        with open("a2.json") as json_file:
            music_data = json.load(json_file)
            db.load_music_data(music_data)


@app.route("/")
def main():
    return render_template('index.html')


if __name__ == "__main__":
    initialise_music_table()
    create_s3_bucket('s3500659-artist-images')
    upload_artist_images()

    # app.run(host="127.0.0.1", port=8080, debug=True)
