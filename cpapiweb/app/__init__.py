import os, platform, json, logging
from flask import Flask
from logging.handlers import RotatingFileHandler

config = {
    'linux_upload':'~/',
    'linux_log':'~/cpapi.log'
}

ostype = platform.system()

if ostype == 'Windows':
    winhome = os.environ['USERPROFILE']
    UPLOAD_FOLDER = winhome
    LOG_FOLDER = winhome + '\\cpapi.log'
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
