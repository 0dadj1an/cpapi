from flask import Flask
import os, platform

ostype = platform.system()

if ostype == 'Windows':
    UPLOAD_FOLDER = 'C:\\'
elif ostype == 'Linux':
    UPLOAD_FOLDER = '/var/tmp/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from app import views
