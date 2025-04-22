from flask import render_template as page
from app import app

@app.route("/")
def index():
    return page("app.html")
