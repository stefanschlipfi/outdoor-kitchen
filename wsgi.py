import sys

path = '/opt/server-monitor/backend/'
if not path in sys.path:
    sys.path.append(path)


from flask_app import app as application
