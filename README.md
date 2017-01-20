
# AWS ELK BOT for SLACK

## Installation and Configuration

### Create Deployment Package Using a Python Environment

```
virtualenv -p python3 elkbot
source elkbot/bin/activate
```

### Install dependencies

Install [Boto3](http://boto3.readthedocs.io/en/latest/guide/configuration.html)
```
pip install boto3
```
Install [AWS4Auth](https://pypi.python.org/pypi/requests-aws4auth)
```
pip install requests-aws4auth
```
Install [Elasticsearch API](https://elasticsearch-py.readthedocs.io/en/master/)
```
pip install elasticsearch
```
Install [Slack](http://slackapi.github.io/python-slackclient/) Client
```
pip install slackclient
```
http://slackapi.github.io/python-slackclient/
https://api.slack.com/methods/chat.postMessage#channels
https://api.slack.com/docs/messages/builder

## Use

Configure Environment Variable
```
export ES_HOST="XYZ.eu-west-1.es.amazonaws.com"
export ES_PORT="443"
export SLACK_TOCKEN="xyz123"
export SLACK_ICON_URL="http://host:port/amazon-elasticsearch.jpg"
export SLACK_CHANNEL="test"
export AWS_PROFILE=""
export AWS_DEFAULT_REGION="eu-west-1"
```
