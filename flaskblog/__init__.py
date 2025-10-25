from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os



app = Flask(__name__, static_url_path='/blog/static')
app.config['SECRET_KEY'] = 'b83887e39f9645a578b9697b9fd62cd8'

# Use environment variable for database URL, fallback to local for development
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://localhost/sebastianrichards_db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['APPLICATION_ROOT'] = '/blog'

# Add middleware to set SCRIPT_NAME for proper URL generation
class PrefixMiddleware(object):
    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)
        else:
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)

app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/blog')



db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskblog import routes
