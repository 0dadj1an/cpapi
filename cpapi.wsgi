import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.append('/usr/lib/python3/dist-packages')
sys.path.append('/usr/local/lib/python3.5/dist-packages')
sys.path.insert(0,'/var/www/cpapi/')

from app import server as application
