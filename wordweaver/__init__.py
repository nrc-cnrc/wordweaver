from flask import Flask
from flask_talisman import Talisman, GOOGLE_CSP_POLICY
import os
from logging.config import dictConfig
from logging import getLogger
from wordweaver.configs import ENV_CONFIG

logger = getLogger('root')

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})

VERSION = '0.0.1'

class Config(object):
    DEBUG = ENV_CONFIG['DEBUG']
    HOST = ENV_CONFIG['HOST']
    PORT = int(ENV_CONFIG['PORT'])
    THREADED = ENV_CONFIG['THREADED']
    FOMA_PYTHON_BINDINGS = ENV_CONFIG['FOMA_PYTHON_BINDINGS']

app = Flask(__name__)

CSP = {}

# Talisman for security
if ENV_CONFIG['security']['default_google_csp']:
    CSP = GOOGLE_CSP_POLICY
else:
    CSP = ENV_CONFIG['security']['custom_csp']
    
Talisman(app, content_security_policy=CSP, content_security_policy_nonce_in=ENV_CONFIG['security']['csp_nonce_in'])

# Configure App
app.config.from_object(Config)
logger.debug("App configured successfully")


import wordweaver.views