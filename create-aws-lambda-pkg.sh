#!/bin/bash
AWS_LAMBDA_FUNCTION_NAME="ELK-Slack-BoT"
echo "Zipping code ..."
zip -9 /var/tmp/lambdapkg.zip bot.py *.json
cd $VIRTUAL_ENV/lib/python3.5/site-packages
zip -r /var/tmp/lambdapkg.zip *
echo "Upload code to AWS Lambda"
aws lambda update-function-code --function-name $AWS_LAMBDA_FUNCTION_NAME --zip-file fileb:///var/tmp/lambdapkg.zip
