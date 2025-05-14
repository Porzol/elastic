from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers import BulkIndexError
from numbers import Number
import time

def upload_documents(documents:list[dict], client:Elasticsearch, index_name:str, chunk_size:int = 20, timeout:int = 60):
    for start in range(0, len(documents), chunk_size):
        chunk = documents[start:start + chunk_size]

        try:
            success_response, fail_response = helpers.bulk(client, chunk, index = index_name, request_timeout = timeout)
        
        except BulkIndexError as e:
            print(f"\n❌ {len(e.errors)} document(s) failed to index:\n")
            for error in e.errors:
                index_error = error.get('index', {})
                print("Reason:", index_error.get('error', {}).get('reason'))
                print("Type:  ", index_error.get('error', {}).get('type'))
                print("Doc:   ", index_error.get('data'))
                print("-" * 40)

def get_match_query(field:str, text:str) -> dict:
    return {
        "match": {
            field: text
        }
    }

def get_semantic_query(field:str, text:str) -> dict:
    return {
        "semantic": {
            "field":field,
            "query":text
        }
    }

def get_term_query(field:str, value:str) -> dict:
    return {
        "term": {
            field: {
                "value": value
            }
        }
    }

def get_numeric_range_query(field:str, gte:Number = None, lte:Number = None) -> dict:
    if not ((gte is None) or (lte is None)):
        if type(gte) is not type(lte):
            raise TypeError(f"Type mismatch: {type(gte).__name__} != {type(lte).__name__}")

    range_body = dict()

    if gte is not None:
        range_body["gte"] = gte
    if lte is not None and (lte >= gte) and lte != 0.0:
        range_body["lte"] = lte
    return {
        "range": {
            field: range_body
        }
    }

def get_bool_query(must_query:list[dict] = None, should_query:list[dict] = None, filter_query:list[dict] = None, must_not_query:list[dict] = None):
    query = {"bool": {}}

    if must_query:
        query["bool"]["must"] = must_query
    if should_query:
        query["bool"]["should"] = should_query
    if filter_query:
        query["bool"]["filter"] = filter_query
    if must_not_query:
        query["bool"]["must_not"] = must_not_query

    return query

def run_query(query_body:dict, client:Elasticsearch, index_name:str):
    RETRIES = 3

    for attempt in range(RETRIES):
        try:
            response = client.search(index = index_name, query = query_body, timeout = f"{120}s")
            context = [hits["_source"] for hits in response["hits"]["hits"]]
            return context
        except Exception as e:
            if attempt < RETRIES - 1:
                time.sleep(2 ** attempt)
            else:
                raise Exception

