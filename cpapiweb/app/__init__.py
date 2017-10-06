from flask import Flask
import os, platform, json

ostype = platform.system()

config = {
    'windows_upload':'C:\\',
    'windows_log':'C:\\cpapi\\cpapi.log',
    'linux_upload':'/var/tmp',
    'linux_log':'/var/log/cpapi/cpapi.log'
}

if ostype == 'Windows':
    UPLOAD_FOLDER = config['windows_upload']
    LOG_FOLDER = config['windows_log']
elif ostype == 'Linux':
    UPLOAD_FOLDER = config['linux_uploa']
    LOG_FOLDER = config['linux_log']

app = Flask(__name__)
app.config['LOG_FOLDER'] = LOG_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from app import views
