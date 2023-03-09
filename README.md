# capturing-missed-lex-utterances

This solution allows you to capture and export missed lex utterances of your bot in last 14 days and their relevant counts to S3 Bucket, this can then be downloaded from S3 bucket.

*Please note:
Always Update the Botversion if published new version.
Always have TO and FROM email verified in SES.


# SUMMARY

1. Event Bridge Rule define "Lambda A" as a Target. 
2. CRON Schedule in Event Bridge Rule, runs the rule every 14 days. 
3. "Lambda A" goes to Amazon Lex and gets all missed utterances in past 14 days and their respective count.
4. get-utterances-view calls made to Lex bot “BotName” for getting missed utterances gets sent back to Lambda A
5. Lambda A sends the details to CSV File. 
6. CSV file is uploaded to S3 bucket by Lambda A. 
7. Lambda B polls/retrieves the file, triggered by S3PutObject API in specific bucket folder. 
8. Lambda B sends the email via SES. 
9. Attachment is sent to end user via Email 
10. End user retrieves the attached file in CSV format.


# Troubleshooting

For all troubleshooting steps if Lambda throws any error, please check the cloudwatch log group and check relevant logs.
Most common errors: Permission Denied errors: Make sure you have provided IAM role of Lambda relevant permissions like reading files from S3 and Lex. 
Timeout Errors- Make sure your Lambda has enough time out to run properly, and adjust as per your utterances in contact center. 
Pagination Errors-If your utterances are more, please change pagination settings in your lambda code, as in how many API calls to be made currently set to 100 at one go, then process next batch in the lambda.
