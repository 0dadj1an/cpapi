# cpapi
General tool for interacting with Check Point Software MGMT Web API.

#### Demo Server  - https://themadhatter.org
* Please **DO NOT** use this server against production environments.
* This server is for **DEMO** purposes only.
* Test Management Server available with **READ ONLY** privilege.
	* IP Address: 10.13.37.1
	* User: cpapidemo
	* Password: cpapipassword
	* Domain: <leave empty>

#### Server Configuration
* git clone https://github.com/themadhatterz/cpapi
* pip3 install flask flask-login requests
* For Linux, create /var/log/cpapi and give ownership to www-data.
  * #sudo mkdir /var/log/cpapi
  * #sudo chown www-data:www-data /var/log/cpapi
* Development Server:
    * python3 ~/cpapi/run.py
* Production Deployment
	* Flask Web Server Deployments
    * http://flask.pocoo.org/docs/0.12/deploying/

#### Features
* Send Custom Crafted API Commands
* Manage Network Objects Including:
	* Hosts
	* Networks
	* Groups
	* Access-Roles
	* Services
	* Gateways and Servers
* Manage Check Point Layered Policy
* Execute commands on Gateways and Servers
