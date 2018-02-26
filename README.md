# cpapi
General tool for interacting with Check Point Software MGMT Web API.

#### Configuration
* git clone https://github.com/themadhatterz/cpapi
* pip3 install flask flask_nav flask-login requests
* Run via:
	* Local development server:
		* python3 ~/cpapi/app/run.py
	* Flask Web Server Deployments
		* http://flask.pocoo.org/docs/0.12/deploying/
* Configure Log Directories under /cpapiweb/app/\_\_init\_\_.py

#### Features
* Send custom commands based on reference guide.
* Add objects. (host, network, group)
* View Check Point Policy.
