import socket
import ujson
from uhttp.client import HTTPConnection


def get(url):
    conn = HTTPConnection(url)
    conn.request("GET", "/")
    resp = conn.getresponse()
    if resp.status == 200:
        resp_json = ujson.loads(resp.read())
    else:
        # handle error...? Raise something?
        print("Error while getting {}!".format(url))

    print(resp)
    print(resp.read())


def post(url, data):
    conn = HTTPConnection(url)
    conn.request("POST", "/", body=ujson.dumps(data))
    resp = conn.getresponse()
    if resp.status == 204:
        return
    elif resp.status == 200:
        return ujson.loads(resp.read())
    else:
        # handle error...? Raise something?
        print("Error while posting data to {}!".format(url))

    print(resp)
    print(resp.read())
