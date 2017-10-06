import logging
from logging.handlers import RotatingFileHandler
from app import app

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler = RotatingFileHandler(app.config['LOG_FOLDER'], maxBytes=10000, backupCount=2)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
app.logger.addHandler(handler)

app.secret_key = 'you-will-never-get-this'
app.run(host='0.0.0.0', port=8080, threaded=True)
