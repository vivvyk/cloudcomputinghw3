import json
import boto3
# import logging

def lambda_handler(event, context):
    # logger = logging.getLogger()
    # logger.setLevel(logging.INFO)
    # logger.info(json.dumps(event))
    # client = boto3.client('transcribe')
    # responseCloseJob = client.delete_transcription_job(
    #     TranscriptionJobName="transcription"
    # )

    bucketname = 'photo-book-b3'
    p = event['fname']
    response = ''
    try:
        #acces transcibed file and find message
        s3 = boto3.resource('s3')
        obj = s3.Object(bucketname, p)
        body = obj.get()['Body'].read()

        result = json.loads(body.decode('utf-8'))
        response = result['results']['transcripts'][0]['transcript'][:-1]

    except:
        #if no transcription.json file return special character
        response = '&'

    #clean up transcribe job and delete transcription.json from bucket
    if response != '&':
        client = boto3.client('transcribe')
        responseCloseJob = client.delete_transcription_job(
            TranscriptionJobName="transcription"
        )
        s3_client = boto3.client('s3')
        responseDelete = s3_client.delete_object(
            Bucket=bucketname,
            Key=p
        )


    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
