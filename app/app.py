from omegaconf import OmegaConf
from psidash.psidash import load_app, load_conf, load_dash, load_components, get_callbacks, assign_callbacks
import flask
from werkzeug.middleware.proxy_fix import ProxyFix
import os
import pathlib



this_dir = pathlib.Path(__file__).parent.resolve()

conf = load_conf(f'{this_dir}/app.yaml')

server = flask.Flask(__name__, # define flask app.server
    static_url_path='', # remove /static/ from url prefixes
    static_folder='static',
    )

# config
server.config.update(
    SECRET_KEY=os.urandom(12),
)


conf['app']['server'] = server

app = load_dash(__name__, conf['app'], conf.get('import'))

server = app.server

# may be needed for iframe embedding
app.server.config.update({
    'SEND_FILE_MAX_AGE_DEFAULT': 0,
    "X_FRAME_OPTIONS": "SAMEORIGIN"
})

app.layout = load_components(conf['layout'], conf.get('import'))

if 'callbacks' in conf:
    callbacks = get_callbacks(app, conf['callbacks'])
    assign_callbacks(callbacks, conf['callbacks'])


if __name__ == '__main__':
    app.run_server(**conf['app.run_server'])

