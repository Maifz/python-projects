"""Flask hello world app."""
from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    """Serve the default page."""
    return '<span style="color:red">Hello World!</span>'
