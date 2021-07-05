from flask import Flask, render_template
from dynamo_db import dynamo_db
import json

app = Flask(__name__)
db = dynamo_db()

# create the music table then load music data from local json file.
if db.table_exist('music') == False:
    table = db.create_music_table()
    if table.count == 0:
        with open("a2.json") as json_file:
            music_data = json.load(json_file)
            db.load_music_data(music_data)







@app.route("/")
def main():
    return render_template('index.html')


if __name__ == "__main__":
    pass
    # app.run(host="127.0.0.1", port=8080, debug=True)
