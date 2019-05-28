# -*- coding: utf-8 -*-
from wordweaver import app
from flask import render_template, url_for

from wordweaver.data.api_data import models
import os
from wordweaver.resources.verb import verb_api
from wordweaver.resources.pronoun import pronoun_api
from wordweaver.resources.affix import affix_api
from wordweaver.resources.conjugate import conjugation_api, conjugation_api_2
from logging import getLogger

logger = getLogger('root')

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
