from flask import Flask
from config import Config
from models import db, Category, Attraction
import routes
import os


def create_app():
    # 创建应用实例
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化数据库
    db.init_app(app)

    # 确保数据库目录存在
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    if db_path:
        db_dir = os.path.dirname(db_path)
        if db_dir:  # 确保目录名不为空
            os.makedirs(db_dir, exist_ok=True)

    # 其余代码保持不变...

    # 注册路由
    routes.init_routes(app)

    # 创建数据库表和初始数据的上下文处理器
    @app.before_first_request
    def create_tables():
        db.create_all()
        # 如果数据库为空，添加初始数据
        if Category.query.count() == 0:
            init_data()

    return app


def init_data():
    """初始化示例数据"""
    # 添加景点类别
    categories = [
        Category(name='中环', description='香港的商业和金融中心'),
        Category(name='尖沙咀', description='购物、餐饮和娱乐中心'),
        Category(name='旺角', description='繁忙的购物区，有很多街市和商场'),
        Category(name='山顶', description='俯瞰香港最佳观景点'),
        Category(name='离岛', description='香港的离岛地区，如大屿山、南丫岛等')
    ]
    for category in categories:
        db.session.add(category)

    # 添加景点
    attractions = [
        # 中环景点
        Attraction(
            name='中环置地广场',
            description='香港最高档的购物中心之一，有众多国际品牌和精品店。',
            image_url='central_landmark.jpg',
            latitude=22.2805,
            longitude=114.1571,
            category_id=1
        ),
        Attraction(
            name='国际金融中心',
            description='香港著名地标，拥有购物中心、办公楼和香港四季酒店。',
            image_url='ifc.jpg',
            latitude=22.2849,
            longitude=114.1577,
            category_id=1
        ),
        # 尖沙咀景点
        Attraction(
            name='尖沙咀海滨长廊',
            description='沿维多利亚港的海滨长廊，可以欣赏香港岛的天际线。',
            image_url='tsim_sha_tsui_promenade.jpg',
            latitude=22.2939,
            longitude=114.1707,
            category_id=2
        ),
        Attraction(
            name='星光大道',
            description='香港的电影主题景点，有香港电影明星的手印和雕像。',
            image_url='avenue_of_stars.jpg',
            latitude=22.2932,
            longitude=114.1712,
            category_id=2
        ),
        # 旺角景点
        Attraction(
            name='女人街',
            description='旺角著名的市集，可以购买各种便宜的商品和纪念品。',
            image_url='ladies_market.jpg',
            latitude=22.3174,
            longitude=114.1707,
            category_id=3
        ),
        # 山顶景点
        Attraction(
            name='太平山顶',
            description='香港最受欢迎的旅游景点之一，可以俯瞰维多利亚港和香港岛的壮丽景色。',
            image_url='victoria_peak.jpg',
            latitude=22.2759,
            longitude=114.1455,
            category_id=4
        ),
        # 离岛景点
        Attraction(
            name='大屿山天坛大佛',
            description='世界上最大的坐佛之一，位于大屿山宝莲禅寺附近。',
            image_url='big_buddha.jpg',
            latitude=22.2536,
            longitude=113.9053,
            category_id=5
        )
    ]
    for attraction in attractions:
        db.session.add(attraction)

    db.session.commit()


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)