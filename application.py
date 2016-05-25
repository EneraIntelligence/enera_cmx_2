from flask.ext.api import FlaskAPI  # importa la clase de flaskapi
from conf.config import LocalConfig  # importa la configuracion la clase que se le da
from modules.authentication import authentication, auth
from modules.enera import enera
from modules import mongo
import os
from flask import Flask, render_template, url_for
from flask import Flask, jsonify

# from flask import Flask, url_for
# from werkzeug.routing import Map, Rule, NotFound, RequestRedirect, BaseConverter
# from flask.ext.script import Manager


application = FlaskAPI(__name__)
# manager = Manager(application)

if 'Hacker' in os.environ:
    application.config.from_object(DevelopConfig)
else:
    application.config.from_object(LocalConfig)

# Blueprint
application.register_blueprint(authentication, url_prefix='/authentication')
application.register_blueprint(enera, url_prefix='/enera')

# we are going to start mongo whit this application
mongo.init_app(application)


@application.route('/')
def index():
    return {'hola': 'index'}


if __name__ == "__main__":
    application.run(
        host=application.config['HOST'],
        debug=application.config['DEBUG'],
        port=application.config['PORT'],
    )
