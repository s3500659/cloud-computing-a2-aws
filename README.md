This project was created as part of assignment 2 of the course Cloud Computing offered by RMIT University. 
The learning objective was to develop a highly scalable web application using AWS services such as: EC2, S3 and DynamoDB.
This app was created using Python 3 and the web framework Flask.

## What does this app do?
It's a simple online music subscription application that allows the user to query songs by their title, artist or year.
Once a song is subscribed, it will be added to their list of subscriptions.
The user is able to add and remove songs as they please. To begin using this app, please first register an account.
Once registered, please log in to begin using the app.

## Update AWS credentials

You will need to have a valid AWS credentials to use this app.
The credential file is typically located here.
```
C:\Users\Name\.aws
```
Open this file using notepad and paste in your credentials.

## How to run the application.

This app will begin by creating all the nessary resources on AWS such as DynamoDb tables and S3 buckets.
This will require the app user to have a valid AWS credentials.

cd into the project folder.
```
cd C:\path\to\the\project\
```

Run the app.
```
python application.py
```


