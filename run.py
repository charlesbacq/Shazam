from Shazamage import shazam_data_base as sdb
from Shazamage import user_data_base as udb
from Shazamage import shazamage as sh
from Shazamage.forms import RegistrationForm, AddSongForm, LoginForm, ShazamageForm, LogoutForm

from flask import render_template, redirect, url_for, flash, Flask
import os
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required, LoginManager, current_user


ALLOWED_EXTENSIONS = {'.flac'}
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.instance_path = os.path.dirname(__file__) + "/static/songs"

login_manager = LoginManager()
login_manager.init_app(app)

Matcher = sh.BruteforceMatcher()  # We can use other matcher like RandomMatcher, BaseMatcher
Matcher.load_db(sdb.db_song_path)  # loading of the database


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
@app.route("/home")
def home():
    """Function that display the template 'home.html'"""
    return render_template('home.html')


@app.route('/shazamage', methods=['GET', 'POST'])
def shazamage():
    """Function that display the template 'shazamage.html', let the user shazam a song
    and add the song the playlist o the user"""
    form = ShazamageForm()
    if form.validate_on_submit():  # if the form have been completed
        f = form.song.data
        filename = secure_filename(f.filename)
        result = Matcher.match(os.path.join(app.instance_path, filename))  # the song return by the Matcher
        flash(f'The song matched is {result[0]} by {result[1]} with a score of {result[2]}'  '.')
        if current_user.is_authenticated:
            udb.add_user_music(udb.db_user_path, current_user.username, result[0], result[1])
        return redirect(url_for('shazamage'))
    return render_template('shazamage.html', title='Shazamage', form=form)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Function that display the template 'uplaod.html' and let the user uplaod a song on the website"""
    form = AddSongForm()
    if form.validate_on_submit():
        f = form.song.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.instance_path, filename))
        sdb.add_a_song(sdb.db_song_path, os.path.join(app.instance_path, filename), form.title.data, form.author.data)
        if current_user.is_authenticated:
            udb.add_user_music(udb.db_user_path, current_user.username, form.title.data, form.author.data)
        flash(f'The song matched is added', 'success')
        return redirect(url_for('home'))
    return render_template('upload.html', title='Upload', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    """Function that display the template 'register.html' and let the user create an account"""
    form = RegistrationForm()
    if form.validate_on_submit():
        udb.add_user(udb.db_user_path, form.username.data, form.email.data, form.password.data)
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@login_manager.user_loader
def load_user(user_id):
    return udb.load_user_from_db(user_id)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """Function that display the template 'login.html' and login a user"""
    form = LoginForm()
    if form.validate_on_submit():
        logout_user()
        is_accurate, user_or_error = udb.assert_connection(form.username.data, form.password.data, udb.db_user_path)
        if is_accurate:
            user = user_or_error
            login_user(user)
            load_user(user)
            flash(f'Congratulations {current_user.username}, you have been logged in ', 'success')
        else:
            error = user_or_error
            if error == 'PasswordError':
                flash('Your password is not correct', 'danger')
            else:
                flash('This username does not exist', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/my_music")
@login_required
def my_music():
    """Function that display the template 'my_music.html' and display the musics of a user"""
    musics = udb.display_user_musics(sdb.db_song_path, current_user.username)
    for music in musics:
        flash(f' Title : {music[0]}, Author : {music[1]} ')
    return render_template('my_music.html', title='My Music')


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    """Function that logout a user"""
    form = LogoutForm()
    if form.validate_on_submit():
        logout_user()
        return redirect(url_for('home'))
    return render_template('logout.html', title='Logout', form=form)


if __name__ == '__main__':
    app.run(debug=False)
