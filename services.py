from elastic import get_bool_query, get_match_query, get_numeric_range_query, get_semantic_query, get_term_query, run_query
from elasticsearch import Elasticsearch

def query_chatlog_index(
    elastic_client:Elasticsearch,
    minimum_revenue:float = None,
    maximum_revenue:float = None,
    chatter_message:str = "",
    chatter_name:str = "",
    fan_message:str = "",
    fan_name:str = "",
    model_name:str = "",
) -> dict:
    must_queries = list()
    if chatter_message is not None and chatter_message != "":
        must_queries.append(get_semantic_query("chatter_message_semantic", chatter_message))
    
    if fan_message is not None and fan_message != "":
        must_queries.append(get_semantic_query("fan_message_semantic", fan_message))
    
    filter_queries = list()
    filter_queries.append(get_numeric_range_query("revenue", minimum_revenue, maximum_revenue))
    
    if fan_name is not None and fan_name != "":
        filter_queries.append(get_term_query("fan_name", fan_name))

    if model_name is not None and model_name != "":
        filter_queries.append(get_term_query("model_name", model_name))

    if chatter_name is not None and chatter_name != "":
        filter_queries.append(get_term_query("chatter_name", chatter_name))

    bool_queries = get_bool_query(must_query = must_queries, filter_query = filter_queries)

    documents = run_query(bool_queries, elastic_client, "fandom-chatlogs")

    return documents

def query_conversation_index(
    elastic_client:Elasticsearch,
    minimum_revenue:float = None,
    maximum_revenue:float = None,
    conversation_message: str = "",
    chatter_name: str = "",
    fan_name: str = "",
    model_name: str = "",
) -> dict:
    global current_llm_context

    must_queries = list()
    if conversation_message is not None and conversation_message != "":
        must_queries.append(get_semantic_query("messages_semantic", conversation_message))
    
    filter_queries = list()
    filter_queries.append(get_numeric_range_query("total_revenue", minimum_revenue, maximum_revenue))
    
    if fan_name is not None and fan_name != "":
        filter_queries.append(get_term_query("fan_name", fan_name))

    if model_name is not None and model_name != "":
        filter_queries.append(get_term_query("model_name", model_name))

    if chatter_name is not None and chatter_name != "":
        filter_queries.append(get_term_query("chatter_name", chatter_name))

    bool_queries = get_bool_query(must_query = must_queries, filter_query = filter_queries)

    documents = run_query(bool_queries, elastic_client, "fandom-conversations")

    current_llm_context = str(documents)

    return documents
