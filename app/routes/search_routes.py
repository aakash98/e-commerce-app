from app.instance.elasticsearch import es
from flask import jsonify, request
from elasticsearch_dsl import Search, Q
from flask import Blueprint
search_app = Blueprint('search_app', __name__)

@search_app.route('/search', methods=['GET'])
def search():
    # Parse filter parameters from request query string
    query = request.args.get('query')
    category = request.args.get('category')
    name = request.args.get('name')
    price_low = request.args.get('price_low')
    price_high = request.args.get('price_high')

    # Construct base Elasticsearch query
    s = Search(using=es, index='product')

    # Apply filters
    if query:
        s = s.query(Q("multi_match", query=query, fields=['name', 'display_name']))
    if category:
        s = s.filter('term', category=category)
    if name:
        s = s.filter('term', name=name)
    if price_low or price_high:
        price_range_query = {}
        if price_low:
            price_range_query['gte'] = price_low
        if price_high:
            price_range_query['lte'] = price_high
        s = s.filter('range', price=price_range_query)

    # Execute Elasticsearch query
    try:
        response = s.execute()
        hits = [hit.to_dict() for hit in response.hits]
        return jsonify(hits)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
