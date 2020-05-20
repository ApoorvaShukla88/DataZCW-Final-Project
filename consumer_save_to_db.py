from kafka import KafkaConsumer, TopicPartition
from json import loads
from sqlalchemy import create_engine
from sqlalchemy import Table
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker

consumer = KafkaConsumer(
    'tweet_sentiment_score',
    bootstrap_servers=['localhost:9092'])

engine = create_engine('mysql+pymysql://root:zipcoder@localhost/twitter')

records_to_insert = list()

metadata = MetaData()
scores = Table('sentiment_score', metadata,
               Column('tweet', Text()),
               Column('id', Integer()),
               Column('location', String(255)),
               Column('timestamp', String(255)),
               Column('score', String(255)),
               )

for message in consumer:
    print(message)
    message = str(message.value)
    details = message.split(",")
    print(details)
    record = {'tweet': details[0], 'id': (details[1]), 'location': details[2], 'timestamp': details[3],
              'score': details[4]}
    records_to_insert.append(record)
    if len(records_to_insert) == 100:
        engine.execute(scores.insert(), records_to_insert)
        records_to_insert = list()
