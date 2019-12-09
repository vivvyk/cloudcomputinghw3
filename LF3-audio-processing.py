import json
import boto3
import logging

def lambda_handler(event, context):
    # logger = logging.getLogger()
    # logger.setLevel(logging.INFO)
    # logger.info(json.dumps(event))

    #run transcribe, save output to photo-book-b3 bucket
    client = boto3.client('transcribe')
    audio_file = event["Records"][0]["s3"]["object"]["key"]
    jobname = "transcription"
    response = client.start_transcription_job(
        TranscriptionJobName=jobname,
        LanguageCode='en-US',
        MediaFormat='wav',
        Media={
            'MediaFileUri': 'https://s3.us-east-1.amazonaws.com/photo-book-b3/'+audio_file
        },
        OutputBucketName='photo-book-b3'
    )

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps("Success")
    }
