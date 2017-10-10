import os, platform, json, logging
from flask import Flask
from logging.handlers import RotatingFileHandler

ostype = platform.system()

config = {
    'windows_upload':'C:\\',
    'windows_log':'C:\\cpapi\\cpapi.log',
    'linux_upload':'/var/tmp/',
    'linux_log':'/var/log/cpapi/cpapi.log'
}

if ostype == 'Windows':
    UPLOAD_FOLDER = config['windows_upload']
    LOG_FOLDER = config['windows_log']
elif ostype == 'Linux':
    UPLOAD_FOLDER = config['linux_upload']
    LOG_FOLDER = config['linux_log']

app = Flask(__name__)
app.config['LOG_FOLDER'] = LOG_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler = RotatingFileHandler(app.config['LOG_FOLDER'], maxBytes=10000, backupCount=2)
handler.setFormatter(formatter)
app.logger.setLevel('DEBUG')
app.logger.addHandler(handler)
app.secret_key = 'you-will-never-get-this'

from app import views
