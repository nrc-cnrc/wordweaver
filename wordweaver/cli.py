import os
import click
import pickle

from flask.cli import FlaskGroup
from tqdm import tqdm

from wordweaver.app import app
from wordweaver import VERSION
from wordweaver.buildtools.swagger_spec_gen import SwaggerSpecGenerator
from wordweaver import __file__ as ww_file
from wordweaver.fst.utils.foma_access_python import foma_access_python as foma_access
from wordweaver.config import ENV_CONFIG
from wordweaver.log import logger
from wordweaver.resources.utils import return_plain


DATA_DIR = os.environ.get('WW_DATA_DIR')

if not DATA_DIR:
    logger.warning(
        'WW_DATA_DIR environment variable is not set, using default sample data instead.')
    DATA_DIR = os.path.join(os.path.dirname(ww_file), 'sample', 'data')

FOMABINS_DIR = os.path.join(DATA_DIR, 'fomabins')

def create_app():
    return app

@click.version_option(version=VERSION, prog_name="wordweaver")
@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    '''Management script for WordWeaver'''

@cli.command()
def spec():
    ''' Update Swagger Specification
    '''
    gen = SwaggerSpecGenerator()
    gen.writeNewData()
    click.echo('Successfully updated Swagger Specification')

@click.option('--pkl/--no-pkl', default=False)
@click.option('--txt/--no-txt', default=False)
@click.option('--plain/--no-plain', default=False)
@click.argument('inp', type=click.STRING, default='')
@click.argument('command', type=click.Choice(['up', 'down', 'lower-words']))
@cli.command()
def foma(command, inp, plain, txt, pkl):
    ''' Interact with foma through command line
    '''
    foma = foma_access(os.path.join(FOMABINS_DIR, ENV_CONFIG["fst_filename"]))
    
    if command == 'up':
        res = [x for x in tqdm(foma.up(inp))]
    elif command == 'down':
        res = [x for x in tqdm(foma.down(inp))]
    elif command == 'lower-words':
        res = [x for x in tqdm(foma.lower_words())]
    
    if plain:
        click.echo('Removing Markup')
        for i, x in tqdm(enumerate(res)):
            res[i] = return_plain(x)

    click.echo(res)

    if pkl:
        with open('res.pkl', 'wb') as f:
            pickle.dump(res, f)
        click.echo('Wrote FST response to pickle')
    
    if txt:
        with open('res.txt', 'w') as f:
            f.writelines('\n'.join(res))
        click.echo('Wrote FST response to text')