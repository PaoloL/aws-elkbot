from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from slackclient import SlackClient
from datetime import date
import json
import requests
import boto3
import os

es_host = os.environ['ES_HOST']
es_port = int(os.environ['ES_PORT'])
es_index = os.environ['ES_INDEX']
slack_token = os.environ['SLACK_TOKEN']
slack_icon_url = os.environ['SLACK_ICON_URL']
slack_channel = os.environ['SLACK_CHANNEL']
slack_app_name = os.environ['SLACK_APP_NAME']
aws_region = os.environ['AWS_DEFAULT_REGION']

def getStatus(es):
    status = es.cluster.health()['status']
    return status

def queryElasticSearch(es,query_file):
    with open(query_file, 'r') as f:
        query = json.load(f)

    res = es.search(index=es_index, body=query)
    return res

def getPercentile(res):
    perc_95_0 =  res['aggregations']['1']['values']['95.0']
    perc_99_8 = res['aggregations']['1']['values']['99.8']
    perc_99_9 = res['aggregations']['1']['values']['99.9']
    percentiles = [perc_95_0, perc_99_8,perc_99_9]
    return percentiles

def getSlowResponses(res):
    total = res['hits']['total']
    return total


def getSuccessConnection(res):
    total = res['hits']['total']
    return total

def formatSlackAttachment(file,daily_values,monthly_values):
    #change color of attachment
    with open(file, 'r') as f:
        attachment = json.load(f)
    #if cluster status is red OR 99.9th percentile > 1
    if (daily_values[0] == 'red') or (daily_values[3][2] >= 1):
        color='#FF0000'
    #if cluster status is yellow OR 99.8th percentile > 1
    if (daily_values[0] == 'yellow') or (daily_values[3][2] >= 1):
        color='#FFC300'
    if daily_values[0] == 'green':
        color='#36a64f'

    #daily values
    attachment[0]['color']=color
    attachment[0]['fields'][1]['value']=daily_values[1]
    attachment[0]['fields'][2]['value']=daily_values[2]
    ##99.5th percentile
    attachment[0]['fields'][3]['value']=daily_values[3][0]
    ##99.8th percentile
    attachment[0]['fields'][4]['value']=daily_values[3][1]
    ##99.9th percentile
    attachment[0]['fields'][5]['value']=daily_values[3][2]

    #monthly values
    attachment[1]['color']=color
    attachment[1]['fields'][0]['value']=monthly_values[1]
    attachment[1]['fields'][1]['value']=monthly_values[2]
    attachment[1]['fields'][2]['value']=monthly_values[3][0]
    attachment[1]['fields'][3]['value']=monthly_values[3][1]
    attachment[1]['fields'][4]['value']=daily_values[3][2]
    return attachment

def pushToSlack(slack_channel, username, msg, attachment):
    sc = SlackClient(slack_token)
    sc.api_call("chat.postMessage",channel=slack_channel, username=username, icon_url=slack_icon_url, as_user="false", text=msg, attachments=attachment)

#lambda execution
def lambda_handler(event, context):
    print("Lambda execution ...")
    session = boto3.Session()
    credentials = session.get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, aws_region, 'es', session_token=credentials.token)
    es = Elasticsearch(hosts=[{'host': es_host, 'port': es_port}],http_auth=awsauth,use_ssl=True,verify_certs=True,connection_class=RequestsHttpConnection)
    es_status = getStatus(es)
    #daily report
    es_daily_percentile = getPercentile(queryElasticSearch(es,'daily_percentile.json'))
    es_daily_slow_response = getSlowResponses(queryElasticSearch(es,'daily_slow_response.json'))
    es_daily_success_connection = getSuccessConnection(queryElasticSearch(es,'daily_success_connection.json'))
    daily_slack_fields = [es_status, es_daily_success_connection, es_daily_slow_response, es_daily_percentile]
    #monthly report
    es_monthly_percentile = getPercentile(queryElasticSearch(es,'monthly_percentile.json'))
    es_monthly_slow_response = getSlowResponses(queryElasticSearch(es,'monthly_slow_response.json'))
    es_monthly_success_connection = getSuccessConnection(queryElasticSearch(es,'monthly_success_connection.json'))
    monthly_slack_fields = [es_status, es_monthly_success_connection, es_monthly_slow_response, es_monthly_percentile]
    attachment = formatSlackAttachment('attachment.json',daily_slack_fields, monthly_slack_fields)

    message =  "Hi <!here> a new report on ELK is available"
    pushToSlack(slack_channel, slack_app_name, message, attachment)

#local execution
def main():
    print("Local Execution ...")
    aws_profile = os.environ['AWS_PROFILE']
    session = boto3.Session(profile_name=aws_profile)
    awsauth = AWS4Auth(str(session.get_credentials().access_key), str(session.get_credentials().secret_key), aws_region, 'es')
    es = Elasticsearch(hosts=[{'host': es_host, 'port': es_port}],http_auth=awsauth,use_ssl=True,verify_certs=True,connection_class=RequestsHttpConnection)
    es_status = getStatus(es)
    #daily report
    es_daily_percentile = getPercentile(queryElasticSearch(es,'daily_percentile.json'))
    es_daily_slow_response = getSlowResponses(queryElasticSearch(es,'daily_slow_response.json'))
    es_daily_success_connection = getSuccessConnection(queryElasticSearch(es,'daily_success_connection.json'))
    daily_slack_fields = [es_status, es_daily_success_connection, es_daily_slow_response, es_daily_percentile]
    #monthly report
    es_monthly_percentile = getPercentile(queryElasticSearch(es,'monthly_percentile.json'))
    es_monthly_slow_response = getSlowResponses(queryElasticSearch(es,'monthly_slow_response.json'))
    es_monthly_success_connection = getSuccessConnection(queryElasticSearch(es,'monthly_success_connection.json'))
    monthly_slack_fields = [es_status, es_monthly_success_connection, es_monthly_slow_response, es_monthly_percentile]
    attachment = formatSlackAttachment('attachment.json',daily_slack_fields, monthly_slack_fields)
    message =  "Hi <!here> a new report on ELK is available"
    pushToSlack(slack_channel, slack_app_name, message, attachment)



if __name__ == "__main__":
    main()
