from app import app
app.secret_key = 'you-will-never-get-this'
app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
