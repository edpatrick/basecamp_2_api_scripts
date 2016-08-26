import urllib
from urllib.request import urlopen
import json
import pprint
from pandas import *
from pandas.io.json import json_normalize

# define pretty print indent
pp = pprint.PrettyPrinter(indent=4)

# gets data about Basecamp topics from Basecamp 2 API
# docs: https://github.com/basecamp/bcx-api
class Topic:


    top_level_url = "https://basecamp.com"
    #add Basecamp username
    uname = '############'
    #add Basecamp password
    pwd = '############'

    def __init__(self, urls):
        self.topic_urls = urls
        self.topic_list = self.get_topic_list(self.topic_urls)

    # returns topic object from Bascampe API
    def request_topic_object(self, url):
        password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, Topic.top_level_url, Topic.uname, Topic.pwd)
        handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
        opener = urllib.request.build_opener(urllib.request.HTTPHandler, handler)
        urllib.request.install_opener(opener)
        topics = urllib.request.urlopen(url)
        return topics

    # returns dataframe of all topics
    def get_topic_list(self, topics):
        topic_list = []
        for url in topics:
            topic_response = self.request_topic_object(url)
            string = topic_response.read().decode('utf-8')
            parsed_json = json.loads(string)
            if not isinstance(topic_list, pandas.DataFrame):
                topic_list = json_normalize(parsed_json)
            else:
                normalized_json = json_normalize(parsed_json)
                topic_list = topic_list.append(normalized_json)

        #update class static variable
        self.topic_list = topic_list
        return topic_list

    def get_topics_by (self, date_type):
        df = self.topic_list
        df['created_at'] = pandas.to_datetime(df['created_at'], format='%Y-%m-%dT%H:%M:%S.%fz')
        df['year'] = df['created_at'].dt.year
        df['month'] = df['created_at'].dt.month
        if date_type is 1:
            return DataFrame({'count': df.groupby([df['year'], df['month']]).size()}).reset_index()
        else:
            return DataFrame({'count': df.groupby(df['year']).size()}).reset_index()

# test class
            
#topics = ['https://basecamp.com/#####/api/v1/projects/#####/topics.json',
#          'https://basecamp.com/#####/api/v1/projects/#####/topics.json?page=2',
#          'https://basecamp.com/#####/api/v1/projects/#####/topics.json?page=3',
#          'https://basecamp.com/#####/api/v1/projects/#####/topics.json.json?page=4'
#          ]

#x = Topic(topics)
#pp.pprint(x.get_topics_by(0))
#y = Topic(topics2)
#pp.pprint(y.get_topics_by())


