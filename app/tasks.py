from app.celery import celery_app
from app.instance.elasticsearch import es

@celery_app.task
def move_to_es(data):
    doc_id = data.pop('_id', None)
    try:
        # Connect to Elasticsearch
        # Index the data in Elasticsearch
        es.index(index='product', body=data)
        return {'status': 'success', 'message': 'Data moved to Elasticsearch successfully'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}