from flask import Flask
import os, platform

ostype = platform.system()

if ostype == 'Windows':
    UPLOAD_FOLDER = 'C:\\'
    LOG_FOLDER = 'C:\\cpapi\cpapi.log'
elif ostype == 'Linux':
    UPLOAD_FOLDER = '/var/tmp/'
    LOG_FOLDER = '/var/log/cpapi/cpapi.log'

app = Flask(__name__)
app.config['LOG_FOLDER'] = LOG_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from app import views
