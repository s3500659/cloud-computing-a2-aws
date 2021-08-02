from flask import Flask, render_template, request, redirect, session, flash, url_for
from dynamo_db import DynamoDbManager
from s3_manager import s3Manager
import json

application = Flask(__name__)
application.secret_key = 'my secret key'
db_client = DynamoDbManager()
s3_client = s3Manager()


def upload_artist_images(bucket_name):
    print(f"Uploading images to bucket {bucket_name}...")

    with open('a2.json') as json_data:
        data = json.load(json_data)
        for item in data['songs']:
            artist = json.dumps(item['artist']).strip('"')
            image_url = json.dumps(item['img_url']).strip('"')

            s3_client.upload_image_url_to_bucket(bucket_name, artist + ".jpg",
                                                 image_url)


def initialise_artist_img_bucket(bucket_name):
    if s3_client.check_bucket_exists(bucket_name) == False:
        s3_client.create_bucket(bucket_name)
        upload_artist_images(bucket_name)


def initialise_subscription_table():
    name = 'user_subscription'
    if db_client.table_exist(name) == False:
        db_client.create_table_double(name, 'email', 'S', 'title', 'S')


def initialise_music_table():
    name = 'music'
    # create the music
    if db_client.table_exist(name) == False:
        db_client.create_table_double(name, 'artist', 'S', 'title', 'S')
        # load music data
        db_client.load_music_data('a2.json')


@application.route("/<title>/<artist>/<year>/subscribe")
def subscribe(title, artist, year):
    user = db_client.get_user(session['user_email'])
    song = db_client.query_music_item(artist, title, year)
    db_client.subscribe_music(user, song[0])

    return redirect(url_for('main_page'))


@application.route("/<title>/remove_sub")
def remove_sub(title):
    db_client.delete_subscription(session['user_email'], title)
    return redirect(url_for('main_page'))


@application.route("/main_page", methods=['GET', 'POST'])
def main_page():
    user = db_client.get_user(session['user_email'])
    subs = db_client.get_subscriptions(user['email'])

    if request.method == 'POST':
        title = request.form['title']
        artist = request.form['artist']
        year = request.form['year']

        response = db_client.query_music_item(artist, title, year)
        if response == []:
            flash('No result is retrieved. Please query again')
            return redirect(url_for('main_page'))
        else:
            return render_template('main_page.html', user=user, subs=subs, response=response)

    return render_template('main_page.html', user=user, subs=subs)


@application.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email'].casefold()
        user_name = request.form['user_name']
        pw = request.form['pw']

        if db_client.get_user(email) != None:
            flash('The email already exists!', 'error')
            return redirect(url_for('register'))

        db_client.create_user(email, user_name, pw)
        return redirect('/')
    return render_template('register.html')


@application.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('main'))


def initialise_login_table():
    name = 'login'
    if db_client.table_exist(name) == False:
        db_client.create_login_table()
        db_client.create_user("vinh@gmail.com", "Vinh Tran", "123")
        db_client.create_user(
            "s35006590@student.rmit.edu.au", "Vinh Tran0", "012345")
        db_client.create_user(
            "s35006591@student.rmit.edu.au", "Vinh Tran1", "123456")
        db_client.create_user(
            "s35006592@student.rmit.edu.au", "Vinh Tran2", "234567")
        db_client.create_user(
            "s35006593@student.rmit.edu.au", "Vinh Tran3", "345678")
        db_client.create_user(
            "s35006594@student.rmit.edu.au", "Vinh Tran4", "456789")
        db_client.create_user(
            "s35006595@student.rmit.edu.au", "Vinh Tran5", "567890")
        db_client.create_user(
            "s35006596@student.rmit.edu.au", "Vinh Tran6", "678901")
        db_client.create_user(
            "s35006597@student.rmit.edu.au", "Vinh Tran7", "789012")
        db_client.create_user(
            "s35006598@student.rmit.edu.au", "Vinh Tran8", "890123")
        db_client.create_user(
            "s35006599@student.rmit.edu.au", "Vinh Tran9", "901234")


@application.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email'].casefold()
        pw = request.form['pw']
        user = db_client.get_user(email)

        if user == None or user['password'] != pw:
            flash('Email or password is invalid!', 'error')
            return redirect(url_for('main'))
        else:
            session['user_email'] = email
            return redirect(url_for('main_page'))

    return render_template('login.html')


@application.route("/")
def main():
    return redirect(url_for('login'))


if __name__ == "__main__":
    initialise_login_table()
    initialise_music_table()
    initialise_subscription_table()
    initialise_artist_img_bucket('s3500659-artist-images')

    from waitress import serve
    serve(application, host="0.0.0.0", port=80)
    # application.run(host="0.0.0.0", port=80, debug=True)
