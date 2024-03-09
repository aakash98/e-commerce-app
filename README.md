# e-commerce-app
Backend Website For E-Commerce App

## Local Installation Of Mongo On Mac

### This Is A Good Guide On How To Setup MongoDB On Mac
https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-os-x/

### You May Also Elect For A Free Account On MongoDB Cloud
https://www.mongodb.com/cloud/atlas/lp/try4

## MongoEngine Configuration On Flask App
### This Is A Good Document For Setting Up Mongo Engine On The App
https://pypi.org/project/flask-mongoengine/

## ElasticSearch Local Installation On Mac

### This is A Very Comprehensive Guide On Setting Up ES
https://www.elastic.co/guide/en/elasticsearch/reference/8.10/run-elasticsearch-locally.html

### curl –insecure -X GET -u elastic:$ELASTIC_PASSWORD "https://localhost:9200/customer/_doc/1?pretty"

## Python Setup
The Project Is Tested Locally On Python 3.9, Running It On Older Packages May Need Tweaking Of Packages In app/requirements.txt

## VirtualEnv Setup
https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/

## Flask Commands
Locally, for testing purposes, you can run the following command

### pip install -r app/requirements.txt
### flask run -p 5001


## In Another Terminal You May Run
### celery -A app.celery worker --loglevel INFO


