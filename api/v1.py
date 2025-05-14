from dependencies import get_elatic_client
from elasticsearch import Elasticsearch
from fastapi import APIRouter, Depends
from schemas import requests
import services

router = APIRouter()

def get_router() -> APIRouter:
    return router

@router.post("/query-chatlog")
def send_query_to_chatlog_index(request: requests.ChatlogIndexRequest, elastic_client: Elasticsearch = Depends(get_elatic_client)):
    documents = services.query_chatlog_index(
    elastic_client,
    request.minimum_revenue,
    request.maximum_revenue,
    request.chatter_message,
    request.chatter_name,
    request.fan_message,
    request.fan_name,
    request.model_name)

    return {
        "success":True,
        "message":documents,
        "request":request
    }

@router.post("/query-conversation")
def send_query_to_conversation_index(request: requests.ConversationIndexRequest, elastic_client: Elasticsearch = Depends(get_elatic_client)):
    documents = services.query_conversation_index(
    elastic_client,
    request.minimum_revenue,
    request.maximum_revenue,
    request.conversation_message,
    request.chatter_name,
    request.fan_name,
    request.model_name)

    return {
        "success":True,
        "message":documents,
        "request":request
    }