# app.py
from flask import Flask
from routes import init_routes
from data_manager import DataManager
import os


def create_app():
    app = Flask(__name__)

    # 配置应用
    app.config['GOOGLE_MAPS_API_KEY'] = ''  # 替换为你的Google Maps API密钥，或保持空字符串

    # 创建CSV文件的路径
    csv_path = os.path.join(app.root_path, 'data', 'attractions.csv')

    # 确保data目录存在
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    # 创建数据管理器
    try:
        data_manager = DataManager(csv_path)
    except Exception as e:
        print(f"加载CSV文件时出错: {e}")
        # 使用样本数据初始化数据管理器
        data_manager = DataManager("")
        data_manager.create_sample_data()

    app.data_manager = data_manager

    # 初始化路由
    init_routes(app)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)