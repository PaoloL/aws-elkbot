from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from slackclient import SlackClient
from datetime import date
import json
import requests
import boto3


es_host = 'search-scorerca-collaudo-utkbmw6aaxk2e5fzwrlrreyesa.eu-west-1.es.amazonaws.com'
es_port = 443
es_index = 'scorerca_elb_logs*'
awsauth = AWS4Auth('AKIAIQPNDBB4SN7N5P4A', 'dqe4KVzDMBX7HOLPUZ2zsBshGZUc1uq9pWrssO/m', 'eu-west-1', 'es')
slack_token = 'xoxp-2154330578-2466889382-128327785552-b3fba7dc3de770392eab51f042d2c6b7'
slack_icon_url = 'http://cloudacademy.com/blog/wp-content/uploads/2015/11/amazon-elasticsearch.jpg'
slack_channel ='test'

def main():
    today = date.today()
    session = boto3.session.Session()
    credentials = session.get_credentials("score-rca")
    print credentials.access_key
    #es = Elasticsearch(hosts=[{'host': es_host, 'port': es_port}],http_auth=awsauth,use_ssl=True,verify_certs=True,connection_class=RequestsHttpConnection)
    #es_status = getStatus(es)
    #es_percentile = get_percentile(queryElasticSearch(es,'percentile.json'))
    #es_slow_response = get_slow_responses(queryElasticSearch(es,'slow_response.json'))
    #es_success_connection = get_success_connection(queryElasticSearch(es,'success_connection.json'))
    message =  "Hi <!here> Cluster Status is " + es_status + \
                "\n" + "Today the total HTTP Connection are " + "*"+str(es_success_connection)+"*" + " only " + "*"+str(es_slow_response)+"*" + " are greather than 1 second" + \
                "\n" + "Today 95th percentile of total_time is " + "*"+str(es_percentile[0])+"*" + \
                "\n" + "Today 99.98th percentile of total_time is " + "*"+str(es_percentile[1])+"*"
    print today
    #pushToSlack(slack_channel,'ELK BoT',message)

def getStatus(es):
    status = es.cluster.health()['status']
    return status

def queryElasticSearch(es,query_file):
    with open(query_file, 'r') as f:
        query = json.load(f)
    res = es.search(index=es_index, body=query)
    return res

def get_percentile(res):
    perc_95_0 =  res['aggregations']['1']['values']['95.0']
    perc_99_98 = res['aggregations']['1']['values']['99.98']
    percentiles = [perc_95_0, perc_99_98]
    return percentiles

def get_slow_responses(res):
    total = res['hits']['total']
    return total


def get_success_connection(res):
    total = res['hits']['total']
    return total


def pushToSlack(slack_channel, username, msg):
    sc = SlackClient(slack_token)
    sc.api_call("chat.postMessage",channel=slack_channel, username=username, icon_url=slack_icon_url, as_user="false", text=msg)

if __name__ == "__main__":
    main()
