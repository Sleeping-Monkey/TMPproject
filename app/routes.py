import flask

from app import app


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/home', methods=["GET", "POST"])
def home():
    return flask.render_template('index.html')
