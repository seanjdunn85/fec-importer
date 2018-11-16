from py2neo import authenticate, Graph
from py2neo.packages.httpstream import http
http.socket_timeout = 24*60*60


class FECGraphClient(object):

    def __init__(self, port, user, password, host='localhost',scheme='http'):
        authenticate(host+":"+port, user, password)
        self.graph = Graph(scheme+"://" +host+":"+port+"/db/data")
        