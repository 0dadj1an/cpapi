import os, base64
from werkzeug import secure_filename

from app import app
from cap import host
from cap import network
from cap import group
from cap import connect

ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    '''Verifies proper file extension.'''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def verify_file(filetype, files):
    '''Verifies that the filename is not blank and prepares the path against relevant OS.'''
    file = files['{}'.format(filetype)]
    filename = secure_filename(file.filename)
    if filename == '':
        error = 'No file provided.'
        return({'status':False, 'report':error})
    if allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        importfile = '{}{}'.format(app.config['UPLOAD_FOLDER'], filename)
        return(importfile)
    else:
        error = 'Wrong file extension.'
        return({'status':False, 'report':error})

def import_check(files, session):
    '''Accepts file input from form and after checks, submits to API.'''
    if 'hosts' in files:
        importfile = verify_file('hosts', files)
        if isinstance(importfile, dict):
            return(importfile)
        else:
            report = host.importhosts(session['ipaddress'], importfile, session['sid'])
            return({'status':True, 'report':report})
    elif 'networks' in files:
        importfile = verify_file('networks', files)
        if isinstance(importfile, dict):
            return(importfile)
        else:
            report = network.importnetworks(session['ipaddress'], importfile, session['sid'])
            return({'status':True, 'report':report})
    elif 'groups' in files:
        importfile = verify_file('groups', files)
        if isinstance(importfile, dict):
            return(importfile)
        else:
            report = group.importgroups(session['ipaddress'], importfile, session['sid'])
            return({'status':True, 'report':report})

def base64_ascii(base64resp):
    '''Converts base64 to ascii for run command/showtask.'''
    asciiresp = base64.b64decode(base64resp).decode('utf-8')
    return(asciiresp)

def clear_session(session):
    '''After any logout, clears session information.'''
    session.pop('sid', None)
    session.pop('ipaddress', None)
    session.pop('apiver', None)
    session.pop('allcommands', None)
    session.pop('allhostlist', None)
    session.pop('allnetlist', None)
    session.pop('allgrouplist', None)
    session.pop('alllayers', None)
    session.pop('alltargets', None)

def add_object_return(response):
    '''Return preperation for add_object to reduce duplication.'''
    try:
        return(response.text)
    except (ValueError, AttributeError) as e:
        return(str(response))
    except Exception as e:
        app.logger.error('FROM VIEWS - Unknown exception - {}'.format(e))
        return('oops')

def add_object(session, request):
    '''Collects form data from add object page.'''
    if 'host' in request.form.keys():
        hostname = request.form.get('hostname')
        ipv4address= request.form.get('ipv4address')
        response = host.addhost(session['ipaddress'], hostname, ipv4address, session['sid'])
        response = add_object_return(response)
        return(response)
    elif 'network' in request.form.keys():
        netname = request.form.get('netname')
        networkip = request.form.get('network')
        mask = request.form.get('mask')
        response = network.addnetwork(session['ipaddress'], netname, networkip, mask, session['sid'])
        response = add_object_return(response)
        return(response)
    elif 'group' in request.form.keys():
        groupname = request.form.get('groupname')
        response = group.addgroup(session['ipaddress'], groupname, session['sid'])
        response = add_object_return(response)
        return(response)
    elif 'addgroup' in request.form.keys():
        hostselection = request.form.getlist('hosts')
        netsselection = request.form.getlist('networks')
        grpsselection = request.form.getlist('groups')
        if hostselection or netsselection or grpsselection:
            members = []
            for hst in hostselection:
                members.append(hst)
            for net in netsselection:
                members.append(net)
            for grp in grpsselection:
                members.append(grp)
            trggselection = request.form.get('trggroup')
            response = group.setgroup(session['ipaddress'], trggselection, members, session['sid'])
            return(response.text)
        else:
            error = 'Please select some group members.'
            return(error)

def logout_session(session, request):
    '''Sends commands to API to discard and logout sessions.'''
    connect.discard(session['ipaddress'], session['sid'])
    connect.logout(session['ipaddress'], session['sid'])
    app.logger.info('Logout from - ip:{} // user:{} // mgmt:{}'.format(request.remote_addr, session['username'], session['ipaddress']))
    clear_session(session)
