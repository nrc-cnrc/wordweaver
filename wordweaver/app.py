import os
import yaml
from flask import Flask, render_template
from flask_talisman import Talisman, GOOGLE_CSP_POLICY
from wordweaver.log import logger
from wordweaver.exceptions import MisconfiguredEnvironment
from wordweaver.resources.verb import verb_api
from wordweaver.resources.pronoun import pronoun_api
from wordweaver.resources.affix import affix_api
from wordweaver.resources.conjugate import conjugation_api, conjugation_api_2
from wordweaver.config import ENV_CONFIG

app = Flask(__name__)

class Config(object):
    DEBUG = ENV_CONFIG['DEBUG']
    HOST = ENV_CONFIG['HOST']
    PORT = int(ENV_CONFIG['PORT'])
    THREADED = ENV_CONFIG['THREADED']

CSP = {}

# Talisman for security
if ENV_CONFIG['security']['default_google_csp']:
    CSP = GOOGLE_CSP_POLICY
else:
    CSP = ENV_CONFIG['security']['custom_csp']
    
# Configure App
Talisman(app, content_security_policy=CSP, content_security_policy_nonce_in=ENV_CONFIG['security']['csp_nonce_in'])
app.config.from_object(Config)

logger.debug("App configured successfully")

# Add Views
app.register_blueprint(affix_api, url_prefix='/api/v1')
app.register_blueprint(pronoun_api, url_prefix='/api/v1')
app.register_blueprint(verb_api, url_prefix='/api/v1')
app.register_blueprint(conjugation_api, url_prefix='/api/v1')
app.register_blueprint(conjugation_api_2, url_prefix='/api/v2')

@app.route('/')
def home():    
    logger.debug("Template rendered successfully")
    return render_template('web.html', gui_imports=ENV_CONFIG['gui_imports'], favicon=ENV_CONFIG['favicon'])

@app.route('/docs')
def swag():
    return render_template('swag.html')
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('web.html'), 404
