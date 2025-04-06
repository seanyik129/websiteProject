from flask import render_template, request, jsonify
from models import Attraction, Category


def init_routes(app):
    @app.route('/')
    def index():
        """首页，展示所有景点类别和热门景点"""
        categories = Category.query.all()
        featured_attractions = Attraction.query.limit(4).all()
        return render_template('index.html',
                               categories=categories,
                               featured_attractions=featured_attractions,
                               google_maps_api_key=app.config['GOOGLE_MAPS_API_KEY'])

    @app.route('/attractions')
    def list_attractions():
        """列出所有景点或按类别筛选"""
        category_id = request.args.get('category_id', type=int)
        categories = Category.query.all()

        if category_id:
            attractions = Attraction.query.filter_by(category_id=category_id).all()
            category = Category.query.get_or_404(category_id)
            return render_template('attractions.html',
                                   attractions=attractions,
                                   category=category,
                                   categories=categories,
                                   google_maps_api_key=app.config['GOOGLE_MAPS_API_KEY'])
        else:
            attractions = Attraction.query.all()
            return render_template('attractions.html',
                                   attractions=attractions,
                                   category=None,
                                   categories=categories,
                                   google_maps_api_key=app.config['GOOGLE_MAPS_API_KEY'])

    @app.route('/attraction/<int:id>')
    def attraction_detail(id):
        """显示单个景点的详细信息"""
        attraction = Attraction.query.get_or_404(id)
        categories = Category.query.all()
        return render_template('attraction.html',
                               attraction=attraction,
                               categories=categories,
                               google_maps_api_key=app.config['GOOGLE_MAPS_API_KEY'])

    @app.route('/directions/<int:id>')
    def get_directions(id):
        """获取到达景点的路线"""
        attraction = Attraction.query.get_or_404(id)
        categories = Category.query.all()
        return render_template('directions.html',
                               attraction=attraction,
                               categories=categories,
                               google_maps_api_key=app.config['GOOGLE_MAPS_API_KEY'])

    @app.route('/api/attractions')
    def api_attractions():
        """API端点：返回所有景点数据"""
        attractions = Attraction.query.all()
        return jsonify([attraction.to_json() for attraction in attractions])