import os
from elasticsearch import Elasticsearch

def get_elatic_client():
    cloud_url = os.getenv("ELASTIC_CLOUD_URL")
    api_key = os.getenv("ELASTIC_API_KEY")

    return Elasticsearch(
    cloud_url,
    api_key = api_key,
    request_timeout = 30
)