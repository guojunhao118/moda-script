# app/__init__.py
from flask import Flask
from app.routes.dynamic_routes import dynamic_routes

def create_app():
    app = Flask(__name__)

    # 注册蓝图
    app.register_blueprint(dynamic_routes, url_prefix='/api/dynamic')  # 所有 dynamic 路由以 /api/dynamic 开头
    # app.register_blueprint(user_routes, url_prefix='/api/user')        # 所有 user 路由以 /api/user 开头

    return app

