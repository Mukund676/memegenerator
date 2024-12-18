from flask import Blueprint, render_template, session, redirect, url_for, request, current_app

from profile import get_profile, update_profile
from memes import save_meme, get_memes, my_memes, delete_meme

import os, time
from werkzeug.utils import secure_filename

meme_bp = Blueprint('memes', __name__)

def upload_image(input_file):
    ts = str(time.time())
    name = ts + secure_filename(input_file.filename)
    full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], name)
    input_file.save(full_path)
    image_url = 'uploads/' + name
    return image_url

@meme_bp.route('/')
def meme_generator():
    if session.get('logged_in'):
        user_id = session.get('user_id')
        profile = get_profile(user_id)
        profile_photo = profile['profileImage']
        return render_template('memes.html', profile_photo=profile_photo)
    else:
        return redirect(url_for('auth.login_page'))

@meme_bp.route("/profile", methods=['GET', 'POST'])
def profile_page():
    if session.get("logged_in"):
        current_id = session.get('user_id')
        if request.method == 'POST':
            input_file = request.files['image']
            image_url = "user.png"
            if input_file.filename:
                file_list = input_file.filename.split('.')
                ext = file_list[-1]
                if ext in ['jpg', 'gif', 'png']:
                    image_url = upload_image(input_file)
            update_profile(current_id, request.form['FirstName'],
                           request.form['LastName'],
                           request.form['Email'],
                           request.form['Bio'],
                           image_url)
        memes = my_memes(current_id)
        return render_template("profile.html", data=get_profile(current_id), memes=memes)
    else:
        return redirect(url_for("auth.login_page"))

@meme_bp.route('/feed')
def meme_feed():
    logged_in = session.get('logged_in')
    memes = get_memes()
    return render_template('feed.html', logged_in=logged_in, memes=memes)

@meme_bp.route('/publish', methods=['POST'])
def publish_meme():
    meme = request.form['image_url']
    if meme == 'uploaded meme':
        input_file = request.files['image']
        image_url = upload_image(input_file)
        http_url = request.environ['HTTP_ORIGIN']
        meme = http_url + url_for('static', filename=image_url)
    user = session.get('user_id')
    save_meme(user, meme)
    return redirect(url_for('memes.meme_feed'))

@meme_bp.route('/delete', methods=['POST'])
def unpublish():
    meme_id = request.form['meme-id']
    delete_meme(meme_id)
    return redirect(url_for('memes.profile_page'))


@meme_bp.route('/upload')
def upload_meme():
    return render_template('uploader.html')

@meme_bp.route('/gifs')
def gif_search():
    if session.get('logged_in'):
        user_id = session.get('user_id')
        profile = get_profile(user_id)
        profile_photo = profile['profileImage']
        return render_template('gifs.html', profile_photo=profile_photo)
    else:
        return redirect(url_for('auth.login_page'))
@meme_bp.route('/about')
def about_page():
    return render_template('about.html')
