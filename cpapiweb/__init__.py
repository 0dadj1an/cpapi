from flask import Flask, session

app = Flask(__name__)
app.secret_key = 'you-will-never-get-this'

from app import views
