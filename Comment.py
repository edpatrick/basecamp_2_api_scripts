import urllib
from urllib.request import urlopen
import json
from pandas import *
#define pretty print indent
import pprint
pp = pprint.PrettyPrinter(indent=4)

# gets data about Basecamp comments from Basecamp 2 API
# docs: https://github.com/basecamp/bcx-api
class Comment:

    top_level_url = "https://basecamp.com"
    #add Basecamp username
    uname = '############'
    #add Basecamp password
    pwd = '############'

    def __init__(self, topic_urls, msg_url):
        self.topic_urls = topic_urls
        self.msg_url = msg_url
        self.api_urls = self.getMsgAPIList(self.topic_urls, self.msg_url)
        self.comment_objects = self.get_comment_objects(self.api_urls)


    # gets http response data from Basecamp API one URL at a time
    def request_api_object(self, url):
        password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, Comment.top_level_url, Comment.uname, Comment.pwd)
        handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
        opener = urllib.request.build_opener(urllib.request.HTTPHandler, handler)
        urllib.request.install_opener(opener)
        topics = urllib.request.urlopen(url)
        return topics

    # loop through topic list to create URLs to request all
    # comments from Basecamp API
    def getMsgAPIList(self, topics, msg_url):
        parsed_json = []
        for url in topics:
            topic_response = self.request_api_object(url)
            string = topic_response.read().decode('utf-8')
            parsed_string = json.loads(string)
            for id in parsed_string:
                element_id = id['topicable']['id']
                api_url = msg_url.format(element_id)
                parsed_json.append(api_url)

        return parsed_json

    # loop through list of topic ids and call function to create list
    # of comment objects
    def get_comment_objects(self, topicList):
        comment_objects = []
        for url in topicList:
            comment_objects.append(self.get_msg_json(url))
        return comment_objects

    # call Basecampe API to get http response object for provided URL
    # then create a JSON object to return
    def get_msg_json(self, url):
        msgs = self.request_api_object(url)
        msgString = msgs.read().decode('utf-8')
        parsedMsg = json.loads(msgString)
        return parsedMsg['comments']

    # extract required data from comment objects
    # return this as a dataframe
    # date_type 0 is year, 1 is month
    def get_dataframe(self, date_type):
        comment_data = []
        for topic_object in self.comment_objects:
            if topic_object:
                for comm_obj in topic_object:
                    date = pandas.to_datetime(comm_obj['created_at'], format='%Y-%m-%dT%H:%M:%S.%fz')
                    year = date.year
                    month = date.month
                    comment_item = {'id': comm_obj['id'], 'year': year, 'month': month}
                    comment_data.append(comment_item)
        dataframe = pandas.DataFrame(comment_data)

        if date_type is 0:
            return pandas.DataFrame({'count': dataframe.groupby(['year']).size()}).reset_index()
        elif date_type is 1:
            return pandas.DataFrame({'count': dataframe.groupby(['year', 'month']).size()}).reset_index()
        else:
            return dataframe

# test class
            
#topics = ['https://basecamp.com/#####/api/v1/projects/#####/topics.json',
#          'https://basecamp.com/#####/api/v1/projects/#####/topics.json?page=2',
#          'https://basecamp.com/#####/api/v1/projects/#####/topics.json?page=3',
#          'https://basecamp.com/#####/api/v1/projects/#####/topics.json.json?page=4'
#          ]
          ]
#msg_url = "https://basecamp.com/#####/api/v1/projects/#####/messages/{}.json"

#x = Comment(topics, msg_url)
#pp.pprint((x.comment_objects))
#pp.pprint(x.get_dataframe())
#pp.pprint(x.get_dataframe(3))
#pp.pprint(x.get_dataframe(0))
#pp.pprint(x.get_dataframe(1))