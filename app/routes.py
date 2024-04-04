from app import app
from flask import render_template, redirect, url_for
from app import db
import sys

@app.route("/")
@app.route("/home")
@app.route("/Home")
def home():
    return render_template('landing-page.html')

@app.route('/text-ex')
def text_example():
    return render_template('text-example.html')
