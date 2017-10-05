import os
from werkzeug import secure_filename

from app import app
from cap import host
from cap import network

ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def import_check(files, session):
    if 'hosts' in files:
        file = files['hosts']
        filename = secure_filename(file.filename)
        if filename == '':
            error = 'No file provided.'
            return({'status':False, 'report':error})
        if allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            hostimportfile = '{}{}'.format(app.config['UPLOAD_FOLDER'], filename)
            report = host.importhosts(session['ipaddress'], hostimportfile, session['sid'])
            return({'status':True, 'report':report})
        else:
            error = 'Wrong file extension.'
            return({'status':False, 'report':error})
    elif 'networks' in files:
        file = files['networks']
        filename = secure_filename(file.filename)
        if filename == '':
            error = 'No file provided.'
            return({'status':False, 'report':error})
        if allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            netimportfile = '{}{}'.format(app.config['UPLOAD_FOLDER'], filename)
            report = network.importnetworks(session['ipaddress'], netimportfile, session['sid'])
            return({'status':True, 'report':report})
        else:
            error = 'Wrong file extension.'
            return({'status':False, 'report':error})

# def base64_ascii(stuff, morestuff):
#     pass
