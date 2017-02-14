
# AWS Lambda BOT - From ELK to SLACK

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
export ES_INDEX"logs*""
export SLACK_TOKEN="xyz123"
export SLACK_ICON_URL="http://host:port/amazon-elasticsearch.jpg"
export SLACK_CHANNEL="test"
export SLACK_APP_NAME="ELK BoT"
export AWS_PROFILE="default"
export AWS_DEFAULT_REGION="eu-west-1"
export
```

Notes: on AWS Lambda the AWS_DEFAULT_REGION Variable is private

Create Zip and Upload file to AWS Lambda
```
chmod 0775 create-aws-lambda-pkg.sh
./create-aws-lambda-pkg.sh
```
