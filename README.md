# cpapi
General tool for interacting with Check Point Software MGMT Web API.

#### Configuration
* git clone https://github.com/themadhatterz/cpapi
* pip3 install flask flask-login requests
* For Linux, create /var/log/cpapi and give ownership to www-data.
  * #sudo mkdir /var/log/cpapi
  * #sudo chown www-data:www-data /var/log/cpapi
* Run via:
  * Local development server:
    * python3 ~/cpapi/run.py
	* Flask Web Server Deployments
    * http://flask.pocoo.org/docs/0.12/deploying/

#### Features
* Send custom commands based on reference guide.
* Add objects. (host, network, group)
* View Check Point Policy.
* Run commands on gateways and servers.
