import json
import boto3
import time
from elasticsearch import Elasticsearch
from decimal import *
import certifi
import logging

def lambda_handler(event, context):

    # logger = logging.getLogger()
    # logger.setLevel(logging.INFO)
    # logger.info(event)

    message = event['q']
    # message = 'show me a squirrel'
    # Send response to lex
    lex_client = boto3.client('lex-runtime')
    response = lex_client.post_text(
        botName="PhotoBookSearch",
        botAlias="PBS",
        userId= "test",
        inputText = message
    )

    #Parse response for keywords
    keywords = []
    keywords.append(response['slots']['firstObject'])
    if response['slots']['secondObject']:
        keywords.append(response['slots']['secondObject'])

    #grab photo names from elastic search
    photo_name_array = []
    for k in keywords:
        es = Elasticsearch("https://vpc-photo-index-ws2mnx42zkb35dr5h4noteotn4.us-east-1.es.amazonaws.com", use_ssl=True, ca_certs=certifi.where())
        res = es.search(index="photos-index", body={"query": {"match": {"labels":k}}})
        for i in range(int(res['hits']['total']['value'])):
            file_name = res['hits']['hits'][i]['_source']['objectKey']
            file_name = file_name.split(".")[0] + ".txt"
            # logger.info(file_name)
            if file_name not in photo_name_array:
                photo_name_array.append(file_name)



    return {
        'statusCode': 200,
        'body': json.dumps(photo_name_array)
    }
