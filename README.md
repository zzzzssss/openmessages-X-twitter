# openmessages X twitter

## Overview
This projdect is designed to explore the role Twitter data played in some social event. An example use case will be:

I am interested in the role Twitter data played when IBM bought red hat.
        * How many unique users posted after the news came out?
        * What precentage of tweets were from official account?
        * How many real-time photos and video were coming out on Twitter after the news came out?
        * How did the followers of IBM and redhat change during and after news came out?

The entire JSON associated with the one single tweet can be seen [here](https://github.com/zzzzssss/openmessages/blob/master/docs/twitter_json_example/twitter_raw_example.json) and [here](https://github.com/zzzzssss/openmessages/blob/master/docs/twitter_json_example/twitter_raw_example.json).
In order to do the analysis, the database structure is designed as follow:
#### Datastructure
The ER diagram is shown below:
![alt text](https://s3.amazonaws.com/testbanking/openmessage.png)

Although most of the Twitter metadata is dynamic, changing tweet-by-tweet. There are stil some metdata which changes slowly or does not change. ex. User's account ID, screen name, language, timezone etc.

So I choose to store the dynamic(info needed to be tracked over time, tweet-by-tweet) and static data(does not change) into different tables as shown in the ER diagram.

**dynamic:**

activities

users_dynamic

hashtag

twitterraw

**static:**

users_static


**twitterraw** is the table for storing the complete raw data. It is inserted to postgreSQL as BLOB(binary) data. In case there is a database problem or not enough infomation is extracted, there is still this redundant data.


#### System Architecture
The architecture of this appication is shown as below:
![alt text](https://s3.amazonaws.com/testbanking/architecture.jpg)



## Getting Started (with docker)

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.


### Prerequisites for Running on local machine
1. install docker

[install docker on MAC OS official guide](https://docs.docker.com/docker-for-mac/install/)

2. Register and Generate twitter api key: [https://apps.twitter.com/](https://apps.twitter.com/)

put **access_token**, **access_token_secret**, **consumer_key**, **consumer_secret**, in `apiserver/config.ini` under `tweepyapi` session:

```
[tweepyapi]
access_token = XXXXXXXXXXXXX
access_token_secret = XXXXXXXXXXX
consumer_key = XXXXXXXXXXXXX
consumer_secret = XXXXXXXXXXXXX
```

### Run
(for simplification, the data is initialized with already streamed data filtered with "trump")

Make sure these two lines in docker-compose.yml:

```
OSTGRES_USER: XXX
POSTGRES_PASSWORD: XXX
```
are the same with these two lines in /apiserver/confg.ini

```
user = XXX
password = XXX
```

cd to the cloned directory(where docker-compose.yml locates) and run `docker-compose up`. The api service will start (if necessary, docker-compose will automatically build the containers).

check link to see all the twitter users in the database:
[localhost:8000/v1/users](http://localhost:8000/v1/users)
![alt text](https://s3.amazonaws.com/testbanking/restAPI.png)



## Getting Started (without docker)

### Prerequisites for Running on local machine(without docker)
(assuming using mac OS for, for other system, please use other methods)
python version should be 2.7
1. install and start kafka
[kafka MAC OS Tutorial](https://medium.com/@Ankitthakur/apache-kafka-installation-on-mac-using-homebrew-a367cdefd273)
```
$ brew cask install java
$ brew install kafka
$ brew services start zookeeper
$ brew services start kafka
```
create topic: tweet

```
$ kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic tweet
```
check topic created

```
$ cd /usr/local/Cellar/kafka/0.10.2.0/libexec/bin
$ ./kafka-topics.sh --list --zookeeper localhost:2181
```
2. install postgresSQL
[postgresSQL MAC OS Tutorial](https://www.codementor.io/engineerapart/getting-started-with-postgresql-on-mac-osx-are8jcopb)

```
$ brew install postgresql
```
start postgresSQL:

```
$ pg_ctl -D /usr/local/var/postgres start && brew services start postgresql
```
check is running:

```
$ postgres -V
```
config postgressql user:

```
$ psql postgres
$ postgres=# \du
$ postgres=# CREATE ROLE *username* WITH LOGIN *PASSWORD* 'quoted password' [OPTIONS]
$ postgres=# \q # quits
```

create database table named twitter:

```
$ psql postgres -U *username* #login with the username just created #Enter password
$ postgres=# CREATE DATABASE twitter;
$ postgres=# GRANT ALL PRIVILEGES ON DATABASE twitter TO *username*; postgres=> \list
$ postgres=# \connect twitter
```
Inside postgres, copy schema in db/Twitterschema.sql to create tables.

check Tables are created and quit:
```
$ postgres=# \dt
$ postgres=# \q # quits
```


### Run
1. go to apiserver/

```
$ cd apiserver
```
2. run worker

```
$ python worker.py
```

3. run streaming server

Register and Generate twitter api key: [https://apps.twitter.com/](https://apps.twitter.com/)

put **access_token**, **access_token_secret**, **consumer_key**, **consumer_secret**, in `apiserver/config.ini` under `tweepyapi` session:

```
[tweepyapi]
access_token = XXXXXXXXXXXXX
access_token_secret = XXXXXXXXXXX
consumer_key = XXXXXXXXXXXXX
consumer_secret = XXXXXXXXXXXXX
```

Run:

```
$ python streaming.py [topic]
```
ex.

```
$ python streaming.py trump USA
```


4. run api server:
change the following three lines (<-for running with docker) in `config.ini`

```
host = localhost
user = shuyang
password = 123
```
To the username and password you just created in the previous step:

```
host = localhost
user = [username]
password = [passowrd]
```
Then run the server

```
$ python main.py
```
check is running: [localhost:8000/v1/users](http://localhost:8000/v1/users)
![alt text](https://s3.amazonaws.com/testbanking/restAPI.png)

## Restful API:
[api documents](https://s3.amazonaws.com/testbanking/index.html)

The swagger.yaml file can be found in folder docs/twitterapi-swagger-doc


Urls to test:
```
path: /users
	Method: GET
		 http://localhost:8000/v1/users/?id=3
         http://localhost:8000/v1/users
         http://localhost:8000/v1/users/3/activities
    Method: PUT
    	  header: Content-Type:application/josn
    	  http://localhost:8000/v1/users
    	  body:
	    	  	{
				  "id": 0,
				  "username": "string",
				  "user_id": "string",
				  "twitter_lang": "string",
				  "location": "string"
				}
```

```
path: /twitterActivities
	Method: GET
		 http://localhost:8000/v1/twitterActivities
         http://localhost:8000/v1/twitterActivities/?id=3
         http://localhost:8000/twitterActivities/?hashtag=trump

```

## Future work:

1. DB design/Data structure: since the user_id and twitter id are getting really big, data type needs to be more efficient instead of using text/bigint
2. kafka and zookeeper: Docker compose (Integertion with apiserver)
3. writing Unit test
3. restful server security, OAth 2.0
4. Deploy to EC2,and integretion with AWS SQS
