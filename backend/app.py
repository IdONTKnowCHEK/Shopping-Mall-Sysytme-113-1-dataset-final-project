import os

from flask import Flask, render_template
from flasgger import Swagger

from api.routes import register_blueprints  # Blueprint 註冊器
from config import config
from models.models import db


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['JSON_AS_ASCII'] = False  # 關閉 ASCII-only

    # 初始化資料庫
    db.init_app(app)

    register_blueprints(app)

    swagger = Swagger(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app


if __name__ == "__main__":
    os.environ['FLASK_ENV'] = 'development'  # 開發模式
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)