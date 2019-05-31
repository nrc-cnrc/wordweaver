import yaml
import json
import click
import os
from wordweaver import VERSION
from flask.cli import FlaskGroup
from flask_talisman import Talisman, GOOGLE_CSP_POLICY
from wordweaver.log import logger
from wordweaver.app import app

def create_app():
    return app

@click.version_option(version=VERSION, prog_name="wordweaver")
@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    """Management script for Word Weaver."""

@cli.command()
@click.argument('config_dir', type=click.Path(exists=True))
@click.argument('data_dir', type=click.Path(exists=True))
def run_app(config_dir, data_dir):
    ENV_CONFIG_PATH = os.path.join(os.path.abspath(config_dir), 'env_config.yaml')
    with open(ENV_CONFIG_PATH, 'r') as stream:
        try:
            ENV_CONFIG = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    class Config(object):
        DEBUG = ENV_CONFIG['DEBUG']
        HOST = ENV_CONFIG['HOST']
        PORT = int(ENV_CONFIG['PORT'])
        THREADED = ENV_CONFIG['THREADED']
        FOMA_PYTHON_BINDINGS = ENV_CONFIG['FOMA_PYTHON_BINDINGS']
        FST_FILENAME = ENV_CONFIG['fst_filename']
        TEST_FST_FILENAME = ENV_CONFIG['test_fst_filename']
        API_KEY = ENV_CONFIG['api_key']
        DATA_DIR = os.path.abspath(data_dir)
        CONFIG_DIR = os.path.abspath(config_dir)

    CSP = {}

    # Talisman for security
    if ENV_CONFIG['security']['default_google_csp']:
        CSP = GOOGLE_CSP_POLICY
    else:
        CSP = ENV_CONFIG['security']['custom_csp']
        
    Talisman(create_app(), content_security_policy=CSP, content_security_policy_nonce_in=ENV_CONFIG['security']['csp_nonce_in'])
    # Configure App
    app = create_app()
    app.config.from_object(Config)
    logger.debug("App configured successfully")
    import wordweaver.views
    return app

@cli.command()
@click.argument('config_dir')
def hello(config_dir):
    print(config_dir)

if __name__ == '__main__':
    cli()