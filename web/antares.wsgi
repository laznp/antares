#!/usr/bin/env python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/html/antares/")
 
from web import antares as application
application.secret_key = 'rahasia'