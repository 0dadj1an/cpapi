import os, base64
from werkzeug import secure_filename

from app import app
from cap import host
from cap import network
from cap import group

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
    elif 'groups' in files:
        file = files['groups']
        filename = secure_filename(file.filename)
        if filename == '':
            error = 'No file provided.'
            return({'status':False, 'report':error})
        if allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            grpimportfile = '{}{}'.format(app.config['UPLOAD_FOLDER'], filename)
            report = group.importgroups(session['ipaddress'], grpimportfile, session['sid'])
            return({'status':True, 'report':report})
        else:
            error = 'Wrong file extension.'
            return({'status':False, 'report':error})

def base64_ascii(base64resp):
    asciiresp = base64.b64decode(base64resp).decode('utf-8')
    return(asciiresp)

def clear_session(session):
    session.pop('sid', None)
    session.pop('apiver', None)
    session.pop('allcommands', None)
    session.pop('allhostlist', None)
    session.pop('allnetlist', None)
    session.pop('allgrouplist', None)
    session.pop('alllayers', None)
    session.pop('alltargets', None)
