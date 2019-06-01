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

config_dir = os.environ.get('WW_CONFIG_DIR')
data_dir = os.environ.get('WW_DATA_DIR')

if not config_dir or not data_dir:
    logger.error(f"WW_CONFIG_DIR is set to {config_dir} and WW_DATA_DIR is set to {data_dir}")
    raise MisconfiguredEnvironment('Sorry, your environment needs to have variables set for the configuration directory (WW_CONFIG_DIR) and the data directory (WW_DATA_DIR) please consult the documentation')

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
    return render_template('web.html')

@app.route('/docs')
def swag():
    return render_template('swag.html')
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('web.html'), 404

if __name__ == '__main__':
    app.run()