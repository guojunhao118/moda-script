import sys
import os
from flask import Flask
from app.database import init_db
from app.routes.dynamic_routes import dynamic_routes  # 导入 dynamic_routes 蓝图

# 将项目根目录添加到系统路径中
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 创建 Flask 应用
app = Flask(__name__)

# 注册路由（将 dynamic_routes 蓝图注册到 Flask 应用中）
app.register_blueprint(dynamic_routes, url_prefix='/api/dynamic')

# 在启动应用时初始化数据库
@app.before_request
def before_request():
    # 确保数据库在首次请求之前初始化
    init_db()

# 默认首页路由
@app.route('/')
def hello_world():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)
