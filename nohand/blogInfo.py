import configparser
import os
class ApiProp:

    CONF_FILE = 'nohand/blogInfo.properties'

    HEADER = "apiBlog"
    KEY_URL = "blog.url"
    # KEY_APP_ID = "blog.app_id"
    # KEY_SCRT_KEY = "blog.secret_key"
    KEY_TOKEN = "blog.access_token"
    
    url = ""
    # app_id = ""
    # scrt_key = ""
    token = ""

    def __init__(self):
        self.conf = configparser.ConfigParser()
        self.loadProp()

    def loadProp(self):
        print("load prop")
        self.conf.read(self.CONF_FILE)

        self.url = self.conf[self.HEADER][self.KEY_URL]
        # self.app_id = self.conf[self.HEADER][self.KEY_APP_ID]
        # self.scrt_key = self.conf[self.HEADER][self.KEY_SCRT_KEY]
        self.token = self.conf[self.HEADER][self.KEY_TOKEN]
    
    def save(self):
        print("save Prop")
        self.conf[self.HEADER][self.KEY_URL] = self.url
        # self.conf[self.HEADER][self.KEY_APP_ID] = self.app_id
        # self.conf[self.HEADER][self.KEY_SCRT_KEY] = self.scrt_key
        self.conf[self.HEADER][self.KEY_TOKEN] = self.token
        self.conf.write(open(self.CONF_FILE, 'w'))

class selProp:
    
    CONF_FILE = 'nohand/blogInfo.properties'

    HEADER = "selBlog"
    KEY_URL = "blog.url"
    KEY_ID = "blog.id"
    KEY_PASSWD = "blog.passwd"
    
    url = ""
    id = ""
    passwd = ""

    def __init__(self):
        self.conf = configparser.ConfigParser()
        self.loadProp()

    def loadProp(self):
        print("load prop")
        self.conf.read(self.CONF_FILE)

        self.url = self.conf[self.HEADER][self.KEY_URL]
        self.id = self.conf[self.HEADER][self.KEY_ID]
        self.passwd = self.conf[self.HEADER][self.KEY_PASSWD]
    
    def save(self):
        print("save Prop")
        self.conf[self.HEADER][self.KEY_URL] = self.url
        # self.conf[self.HEADER][self.KEY_APP_ID] = self.app_id
        # self.conf[self.HEADER][self.KEY_SCRT_KEY] = self.scrt_key
        self.conf[self.HEADER][self.KEY_ID] = self.id
        self.conf[self.HEADER][self.KEY_PASSWD] = self.passwd
        self.conf.write(open(self.CONF_FILE, 'w'))