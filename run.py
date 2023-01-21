import flask_login
from flask import flash
from Shazamage.forms import RegistrationForm, AddSongForm, LoginForm, ShazamageForm, LogoutForm
from flask import Flask
from flask import render_template, redirect, url_for, request, send_from_directory
import os
from werkzeug.utils import secure_filename
from Shazamage.model import *
from Shazamage import shazam_data_base as sdb
from Shazamage import user_data_base as udb
from Shazamage import shazamage as sh

from flask_login import login_user, logout_user, login_required, LoginManager, current_user, login_fresh
from os.path import splitext
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
login_manager = LoginManager()
login_manager.init_app(app)

Matcher = sh.BruteforceMatcher()
Matcher.load_db(sdb.db_song_path)
print('test_start')

#user = None



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')



## Cette page permet de upload une music et d'appliquer l'algo Shazam que Simon a fait, mais je comprends pas comment appliquer une fonction sur la page html,
## enfin comment relier l'algo Shazam à la page html où j'ai crée le bouton "Compare"

## Aussi lorsque je veux upload une chanson en mp3, cela fonctionne (elle arrive bien dans le fichier son.mp3 mais cela ne fonctionne pas pour un fichier flac (Simon ne peut utiliser
## que des fichiers flac
UPLOAD_FOLDER = './static/sons'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['mp3'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = AddSongForm()
    if form.validate_on_submit():
        f = form.song.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            app.instance_path, filename
        ))
        sdb.add_a_song(sdb.db_song_path, os.path.join(app.instance_path, filename), form.title.data, form.author.data)
        if current_user.is_authenticated:
            udb.add_user_music(udb.db_user_path,current_user.username,form.title.data,form.author.data)
        flash(f'The song matched is added', 'success')
        return redirect(url_for('home'))
    return render_template('upload.html', title='Upload', form=form)

@app.route('/shazamage',methods=['GET', 'POST'])
def shazamage():
    form = ShazamageForm()
    if form.validate_on_submit():
        f = form.song.data
        filename = secure_filename(f.filename)
        #f.save(os.path.join(app.instance_path, filename))
        result = Matcher.match(os.path.join(app.instance_path, filename))
        flash(f'The song matched is {result[0]} by {result[1]} with a score of {result[2]}'  '.')
        if current_user.is_authenticated :
            udb.add_user_music(udb.db_user_path, current_user.username, result[0], result[1])
        return redirect(url_for('shazamage'))
    return render_template('shazamage.html',title='Shazamage',form=form)


## Cette page sert pour aaffciher toutes les musiques d'un utlisateur, j'essaye de céer un tableau grâce à une base de donnée mais je galère (j'ai mis un premier test en mode commentée dans my_music.html)
## mais il faut une base de donnée et j'arrive pas à créer une base de donnée d'essais.

@app.route("/my_music")
@login_required
def my_music():
    musics = udb.display_user_musics(sdb.db_song_path, current_user.username)
    for music in musics:
        flash(f' Title : {music[0]}, Author : {music[1]} ')
    return render_template('my_music.html', title='My Music')



## Permet de créer un compte, j'ai mis deux fonctions : la première c'est celle du tuto qui utilise pas peewee, la deuxième c'est celle que j'ai crée,
## il faut voir si elle fonctionne mais il faut une base de donnée et j'ai du mal à comprendre comment en faire une(même d'essais)
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # user = User(username=form.username.data, email=form.email.data,password=form.password.data)
        udb.add_user(udb.db_user_path, form.username.data, form.email.data, form.password.data)
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

## Permet de login, j'ai mis deux fonctions : la première c'est celle du tuto qui utilise pas peewee, la deuxième c'est celle que j'ai crée,
## il faut voir si elle fonctionne mais il faut une base de donnée et j'ai du mal à comprendre comment en faire une(même d'essais)

@login_manager.user_loader
def load_user(user_id):
    print('load_user', user_id)
    return udb.load_user_from_db(user_id)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        logout_user()
        bool, user = udb.assert_connection(form.username.data, form.password.data, udb.db_user_path)
        if bool:
            print(user,type(user),user.id,user.username)
            login_user(user)
            load_user(user)
            flash(f'Congratulations {current_user.username}, you have been logged in ', 'success')
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    form = LogoutForm()
    if form.validate_on_submit():
        logout_user()
        return redirect(url_for('home'))
    return render_template('logout.html', title='Logout', form=form)


if __name__ == '__main__':
    app.run(debug=False)