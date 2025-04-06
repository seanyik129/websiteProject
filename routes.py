# routes.py
from flask import render_template, request, jsonify, abort, redirect, url_for


def init_routes(app):
    @app.route('/')
    def index():
        """首页，展示所有类别和特色景点"""
        categories = app.data_manager.get_unique_categories()
        featured_attractions = app.data_manager.get_featured_attractions(8)  # 增加到8个推荐景点
        return render_template('index.html',
                               categories=categories,
                               featured_attractions=featured_attractions,
                               google_maps_api_key=app.config['GOOGLE_MAPS_API_KEY'])

    @app.route('/attractions')
    def list_attractions():
        """列出所有景点或按类别/区域筛选"""
        category = request.args.get('category')
        district = request.args.get('district')
        all_categories = app.data_manager.get_unique_categories()

        if category:
            attractions = app.data_manager.get_attractions_by_category(category)
            return render_template('attractions.html',
                                   attractions=attractions,
                                   current_category=category,
                                   current_district=None,
                                   categories=all_categories,
                                   google_maps_api_key=app.config['GOOGLE_MAPS_API_KEY'])
        elif district:
            attractions = app.data_manager.get_attractions_by_district(district)
            return render_template('attractions.html',
                                   attractions=attractions,
                                   current_category=None,
                                   current_district=district,
                                   categories=all_categories,
                                   google_maps_api_key=app.config['GOOGLE_MAPS_API_KEY'])
        else:
            attractions = app.data_manager.get_all_attractions()
            return render_template('attractions.html',
                                   attractions=attractions,
                                   current_category=None,
                                   current_district=None,
                                   categories=all_categories,
                                   google_maps_api_key=app.config['GOOGLE_MAPS_API_KEY'])

    @app.route('/attraction/<int:id>')
    def attraction_detail(id):
        """显示单个景点的详细信息"""
        attraction = app.data_manager.get_attraction_by_id(id)
        if not attraction:
            abort(404)

        categories = app.data_manager.get_unique_categories()
        return render_template('attraction.html',
                               attraction=attraction,
                               categories=categories,
                               google_maps_api_key=app.config['GOOGLE_MAPS_API_KEY'],
                               data_manager=app.data_manager)

    @app.route('/directions/<int:id>')
    def get_directions(id):
        """获取到达景点的路线"""
        attraction = app.data_manager.get_attraction_by_id(id)
        if not attraction:
            abort(404)

        categories = app.data_manager.get_unique_categories()
        return render_template('directions.html',
                               attraction=attraction,
                               categories=categories,
                               google_maps_api_key=app.config['GOOGLE_MAPS_API_KEY'])

    @app.route('/random-route', methods=['GET', 'POST'])
    def random_route():
        """生成随机路线"""
        count = request.args.get('count', type=int, default=5)
        if count < 1:
            count = 5

        route = app.data_manager.generate_random_route(count)
        categories = app.data_manager.get_unique_categories()

        return render_template('random_route.html',
                               route=route,
                               categories=categories,
                               count=count,
                               google_maps_api_key=app.config['GOOGLE_MAPS_API_KEY'])

    @app.route('/api/attractions')
    def api_attractions():
        """API端点：返回所有景点数据"""
        attractions = app.data_manager.get_all_attractions()
        return jsonify(attractions)