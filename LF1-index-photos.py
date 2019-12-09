import json
import boto3
import time
import certifi
from elasticsearch import Elasticsearch
from decimal import *
import logging

#get labels from rekognition
def detect_labels(photo, bucket):

    '''
    https://docs.aws.amazon.com/rekognition/latest/dg/labels-detect-labels-image.html
    '''

    client=boto3.client('rekognition')

    response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},
        MaxLabels=10)

    names = []
    print('Detected labels for ' + photo)
    for label in response['Labels']:
        names.append(label['Name'])
    return names


def lambda_handler(event, context):

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info(json.dumps(event))


    photo = event["Records"][0]["s3"]["object"]["key"]
    # bucket = event["Records"][0]["s3"]["bucket"]["name"]

    #do not call rekognition on txt files
    if photo.split('.')[1] == 'txt':
        return {
            'statusCode': 200,
            'body': json.dumps("Text File Not Added To ES")
        }

    # photo = 'ttqpadzk04l8i4pb4xn6.jpeg'
    bucket = 'photo-book-b2'
    labelList=detect_labels(photo, bucket)
    logger.info(labelList)

    labelEntry = {}
    labelEntry["objectKey"] = photo
    labelEntry["bucket"] = bucket
    labelEntry["createdTimestamp"] = time.time()
    labelEntry["labels"] =  labelList

    #index photo in elasticsearch
    es = Elasticsearch("https://vpc-photo-index-ws2mnx42zkb35dr5h4noteotn4.us-east-1.es.amazonaws.com", use_ssl=True, ca_certs=certifi.where())
    res = es.index(index='photos-index',doc_type='photo', id=int(time.time()), body=labelEntry)

    return {
        'statusCode': 200,
        'body': json.dumps("SUCCESS")
    }
