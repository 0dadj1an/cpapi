from flask import render_template
from app import app
from flask import request

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        print (request.get_data())
    return (render_template('login.html', title='Sign In'))
