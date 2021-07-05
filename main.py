from flask import Flask, render_template
from dynamo_db import dynamo_db
from s3_manager import s3_manager
import json

app = Flask(__name__)
db = dynamo_db()
s3_client = s3_manager()


def upload_artist_images(bucket_name):
    with open('a2.json') as json_data:
            data = json.load(json_data)
            for item in data['songs']:
                artist = json.dumps(item['artist']).strip('"')
                image_url = json.dumps(item['img_url']).strip('"')

                s3_client.upload_image_url_to_bucket(bucket_name, artist + ".jpg", 
                        image_url)


def initialise_s3_bucket():
    s3_client.create_bucket('s3500659-artist-images')

    if s3_client.count_objects_in_bucket('s3500659-artist-images') == 0:
        upload_artist_images('s3500659-artist-images')


def initialise_music_table():
    # create the music
    if db.table_exist('music') == False:
        db.create_music_table()
        # load music data
        db.load_music_data('a2.json')



@app.route("/")
def main():
    return render_template('index.html')


if __name__ == "__main__":
    initialise_music_table()
    initialise_s3_bucket()



    # app.run(host="127.0.0.1", port=8080, debug=True)
