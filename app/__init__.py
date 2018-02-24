import os
import platform
import logging
from flask import Flask
from logging.handlers import RotatingFileHandler

ostype = platform.system()

if ostype == 'Windows':
    LOG_FOLDER = '{}\\'.format(os.getcwd())
if ostype == 'Linux':
    LOG_FOLDER = '/var/log/cpapi/'

app = Flask(__name__)
app.config['LOG_FOLDER'] = "{}cpapi.log".format(LOG_FOLDER)

formatter = logging.Formatter('%(asctime)s %(levelname)s - '
                              '%(filename)s:%(funcName)s:%(lineno)d - '
                              '%(message)s')
handler = RotatingFileHandler(
    app.config['LOG_FOLDER'], maxBytes=10000000, backupCount=10)
handler.setFormatter(formatter)
app.logger.setLevel('DEBUG')
app.logger.addHandler(handler)
app.secret_key = os.urandom(25)

from app import views
