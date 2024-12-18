from flask import Flask, render_template, abort

from users import create_table
from profile import setup_profile
from memes import setup_memes

from auth import auth_bp
from meme_generator import meme_bp

app = Flask('app')

app.secret_key = 'weukyrfiwNER8WF7BIY3i4weur628YRNTWH3875T6NQ3IY'

upload_folder = 'static/uploads'
app.config['UPLOAD_FOLDER'] = upload_folder

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(meme_bp)

with app.app_context():
    create_table()
    setup_profile()
    setup_memes()
app.run(host='0.0.0.0', port=1232)
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error)

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html', error=error)

@app.errorhandler(410)
def gone_error(error):
    return render_template('410.html', error=error)

@app.route('/secret')
def secret_page():
    abort(403)

@app.route('/temp')
def temp_page():
    abort(410)
