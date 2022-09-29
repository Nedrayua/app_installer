from app import app
import view

from config import WEBAPP_HOST, WEBAPP_PORT
from api.api import api

app.register_blueprint(api, url_prefix='/api')


if __name__ == '__main__':
    app.run(host=WEBAPP_HOST, port=WEBAPP_PORT)
